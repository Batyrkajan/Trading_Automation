import pytest
import asyncio

from app.thinker import should_execute_trade


@pytest.mark.asyncio
async def test_should_execute_trade_no_duplicate_signal():
    assert await should_execute_trade("buy", last_executed_signal="sell") is True
    assert await should_execute_trade("sell", last_executed_signal="buy") is True
    assert await should_execute_trade("buy", last_executed_signal="hold") is True
    assert await should_execute_trade("hold", last_executed_signal="buy") is True


@pytest.mark.asyncio
async def test_should_execute_trade_duplicate_signal_buy():
    assert await should_execute_trade("buy", last_executed_signal="buy") is False


@pytest.mark.asyncio
async def test_should_execute_trade_duplicate_signal_sell():
    assert await should_execute_trade("sell", last_executed_signal="sell") is False


@pytest.mark.asyncio
async def test_should_execute_trade_duplicate_signal_hold():
    assert await should_execute_trade("hold", last_executed_signal="hold") is True


@pytest.mark.asyncio
async def test_should_execute_trade_delay():
    start_time = asyncio.get_event_loop().time()
    await should_execute_trade("buy", last_executed_signal="sell")
    end_time = asyncio.get_event_loop().time()
    assert (end_time - start_time) >= 1.0


@pytest.mark.asyncio
async def test_should_execute_trade_rsi_threshold_met():
    assert await should_execute_trade(
        "buy",
        min_rsi_change_threshold=5.0,
        current_indicators={"RSI_14": 60.0},
        last_indicators={"RSI_14": 50.0}
    ) is True


@pytest.mark.asyncio
async def test_should_execute_trade_rsi_threshold_not_met():
    assert await should_execute_trade(
        "buy",
        min_rsi_change_threshold=5.0,
        current_indicators={"RSI_14": 52.0},
        last_indicators={"RSI_14": 50.0}
    ) is False


@pytest.mark.asyncio
async def test_should_execute_trade_rsi_threshold_not_provided():
    assert await should_execute_trade(
        "buy",
        current_indicators={"RSI_14": 52.0},
        last_indicators={"RSI_14": 50.0}
    ) is True
