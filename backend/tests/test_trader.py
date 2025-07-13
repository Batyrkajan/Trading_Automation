import pytest
from unittest.mock import MagicMock

from app.trader import AlpacaTrader
from app.config import settings

# Mock Alpaca API base URL (not directly used for mocking SDK methods, but good for context)
ALPACA_API_BASE_URL = "https://paper-api.alpaca.markets"


@pytest.fixture
def trader():
    # Create a mock for the Alpaca REST API client
    mock_alpaca_api = MagicMock()

    # Mock the methods that AlpacaTrader will call
    # These methods are synchronous in the actual alpaca-trade-api client
    mock_alpaca_api.submit_order = MagicMock()
    mock_alpaca_api.get_account = MagicMock()
    mock_alpaca_api.get_position = MagicMock()

    # Temporarily set API keys for testing (though they won't be used by the mocked client)
    settings.ALPACA_API_KEY = "test_key"
    settings.ALPACA_SECRET_KEY = "test_secret"

    # Create an instance of AlpacaTrader and inject the mocked API client
    trader_instance = AlpacaTrader()
    trader_instance.api = mock_alpaca_api
    return trader_instance


@pytest.mark.asyncio
async def test_get_account_info_success(trader: AlpacaTrader):
    # Configure the mock to return a successful account object
    mock_account = MagicMock(status="ACTIVE", equity="100000.0",
                             buying_power="50000.0")
    trader.api.get_account.return_value = mock_account

    account = await trader.get_account_info()
    assert account is not None
    assert account.status == "ACTIVE"
    assert float(account.equity) == 100000.0
    trader.api.get_account.assert_called_once()  # Verify the mock was called


@pytest.mark.asyncio
async def test_get_account_info_failure(trader: AlpacaTrader):
    # Configure the mock to raise an exception
    trader.api.get_account.side_effect = Exception("API error")

    account = await trader.get_account_info()
    assert account is None
    trader.api.get_account.assert_called_once()


@pytest.mark.asyncio
async def test_place_order_success(trader: AlpacaTrader):
    # Configure the mock to return a successful order object
    mock_order = MagicMock(id="order_id_123", symbol="AAPL", qty="1",
                           side="buy", type="market")
    trader.api.submit_order.return_value = mock_order

    order = await trader.place_order(symbol="AAPL", qty=1, side="buy")
    assert order is not None
    assert order.id == "order_id_123"
    assert order.symbol == "AAPL"
    trader.api.submit_order.assert_called_once_with(
        symbol="AAPL", qty=1, side="buy", type="market", time_in_force="gtc"
    )


@pytest.mark.asyncio
async def test_place_order_failure(trader: AlpacaTrader):
    # Configure the mock to raise an exception
    trader.api.submit_order.side_effect = Exception("Invalid order parameters.")

    order = await trader.place_order(symbol="INVALID", qty=1, side="buy")
    assert order is None
    trader.api.submit_order.assert_called_once()


@pytest.mark.asyncio
async def test_get_position_success(trader: AlpacaTrader):
    # Configure the mock to return a successful position object
    mock_position = MagicMock(symbol="AAPL", qty="10", avg_entry_price="150.0")
    trader.api.get_position.return_value = mock_position

    position = await trader.get_position(symbol="AAPL")
    assert position is not None
    assert position.symbol == "AAPL"
    assert int(position.qty) == 10
    trader.api.get_position.assert_called_once_with("AAPL")


@pytest.mark.asyncio
async def test_get_position_not_found(trader: AlpacaTrader):
    # Configure the mock to raise an exception (Alpaca API raises for no position)
    trader.api.get_position.side_effect = Exception("position not found")

    position = await trader.get_position(symbol="MSFT")
    assert position is None
    trader.api.get_position.assert_called_once_with("MSFT")
