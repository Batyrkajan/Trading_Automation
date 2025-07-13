import pytest
import respx  # noqa: F401
import httpx
from respx import MockRouter

from app.analyzer import get_trading_signal
from app.models import DeepSeekErrorResponse


@pytest.mark.asyncio
async def test_get_trading_signal_buy(respx_mock: MockRouter):
    respx_mock.post("https://api.deepseek.com/chat/completions").mock(
        return_value=httpx.Response(200, json={
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1678886400,
            "model": "deepseek-chat",
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": "buy"},
                "finish_reason": "stop"
            }],
            "usage": {"prompt_tokens": 10, "completion_tokens": 1,
                      "total_tokens": 11}
        })
    )

    signal = await get_trading_signal(indicators={"RSI_14": 30.0, "EMA_20": 100.0},
                                      api_key="test_key")
    assert signal == "buy"


@pytest.mark.asyncio
async def test_get_trading_signal_sell(respx_mock: MockRouter):
    respx_mock.post("https://api.deepseek.com/chat/completions").mock(
        return_value=httpx.Response(200, json={
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1678886400,
            "model": "deepseek-chat",
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": "sell"},
                "finish_reason": "stop"
            }],
            "usage": {"prompt_tokens": 10, "completion_tokens": 1,
                      "total_tokens": 11}
        })
    )

    signal = await get_trading_signal(indicators={"RSI_14": 70.0, "EMA_20": 200.0},
                                      api_key="test_key")
    assert signal == "sell"


@pytest.mark.asyncio
async def test_get_trading_signal_hold(respx_mock: MockRouter):
    respx_mock.post("https://api.deepseek.com/chat/completions").mock(
        return_value=httpx.Response(200, json={
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1678886400,
            "model": "deepseek-chat",
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": "hold"},
                "finish_reason": "stop"
            }],
            "usage": {"prompt_tokens": 10, "completion_tokens": 1,
                      "total_tokens": 11}
        })
    )

    signal = await get_trading_signal(indicators={"RSI_14": 50.0, "EMA_20": 150.0},
                                      api_key="test_key")
    assert signal == "hold"


@pytest.mark.asyncio
async def test_get_trading_signal_api_error(respx_mock: MockRouter):
    respx_mock.post("https://api.deepseek.com/chat/completions").mock(
        return_value=httpx.Response(401, json={
            "error": {"message": "Invalid API key",
                      "type": "authentication_error",
                      "code": "invalid_api_key"}
        })
    )

    response = await get_trading_signal(indicators={"RSI_14": 50.0, "EMA_20": 150.0},
                                        api_key="invalid_key")
    assert isinstance(response, DeepSeekErrorResponse)
    assert "Invalid API key" in response.error.message
    assert response.error.type == "http_error"


@pytest.mark.asyncio
async def test_get_trading_signal_network_error(respx_mock: MockRouter):
    respx_mock.post("https://api.deepseek.com/chat/completions").mock(
        side_effect=httpx.RequestError("Connection refused",
                                       request=httpx.Request("POST",
                                                             "https://api.deepseek.com/chat/completions"))
    )

    response = await get_trading_signal(indicators={"RSI_14": 50.0, "EMA_20": 150.0},
                                        api_key="test_key")
    assert isinstance(response, DeepSeekErrorResponse)
    assert response.error.type == "network_error"
    assert "Connection refused" in response.error.message


@pytest.mark.asyncio
async def test_get_trading_signal_unexpected_signal_format(respx_mock: MockRouter):
    respx_mock.post("https://api.deepseek.com/chat/completions").mock(
        return_value=httpx.Response(200, json={
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1678886400,
            "model": "deepseek-chat",
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": "unexpected_format"},
                "finish_reason": "stop"
            }],
            "usage": {"prompt_tokens": 10, "completion_tokens": 1,
                      "total_tokens": 11}
        })
    )

    response = await get_trading_signal(indicators={"RSI_14": 50.0, "EMA_20": 150.0},
                                        api_key="test_key")
    assert isinstance(response, DeepSeekErrorResponse)
    assert response.error.type == "parsing_error"
    assert "Unexpected signal format" in response.error.message


@pytest.mark.asyncio
async def test_get_trading_signal_empty_choices(respx_mock: MockRouter):
    respx_mock.post("https://api.deepseek.com/chat/completions").mock(
        return_value=httpx.Response(200, json={
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1678886400,
            "model": "deepseek-chat",
            "choices": [],
            "usage": {"prompt_tokens": 10, "completion_tokens": 0,
                      "total_tokens": 10}
        })
    )

    response = await get_trading_signal(indicators={"RSI_14": 50.0, "EMA_20": 150.0},
                                        api_key="test_key")
    assert isinstance(response, DeepSeekErrorResponse)
    assert response.error.type == "parsing_error"
    assert "No signal found in DeepSeek response." in response.error.message


@pytest.mark.asyncio
async def test_get_trading_signal_empty_message_content(respx_mock: MockRouter):
    respx_mock.post("https://api.deepseek.com/chat/completions").mock(
        return_value=httpx.Response(200, json={
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1678886400,
            "model": "deepseek-chat",
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": ""},
                "finish_reason": "stop"
            }],
            "usage": {"prompt_tokens": 10, "completion_tokens": 0,
                      "total_tokens": 10}
        })
    )

    response = await get_trading_signal(indicators={"RSI_14": 50.0, "EMA_20": 150.0},
                                        api_key="test_key")
    assert isinstance(response, DeepSeekErrorResponse)
    assert response.error.type == "parsing_error"
    assert "No signal found in DeepSeek response." in response.error.message
