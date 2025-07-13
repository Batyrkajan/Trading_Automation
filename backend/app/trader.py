from alpaca_trade_api.rest import REST
from alpaca_trade_api.common import URL

from app.config import settings
from app.utils import logger


class AlpacaTrader:
    def __init__(self):
        self.api = REST(
            settings.ALPACA_API_KEY,
            settings.ALPACA_SECRET_KEY,
            URL(settings.APCA_API_BASE_URL)
        )
        logger.info("AlpacaTrader initialized with paper trading account.")

    async def place_order(
        self, symbol: str, qty: float, side: str, type: str = "market",
        time_in_force: str = "gtc"
    ):
        """
        Places a trade order with Alpaca.

        Args:
            symbol (str): The trading symbol (e.g., 'AAPL').
            qty (int): The quantity of shares.
            side (str): 'buy' or 'sell'.
            type (str): Order type (e.g., 'market', 'limit').
            time_in_force (str): Time in force (e.g., 'gtc', 'day').

        Returns:
            Order: The placed order object.
        """
        try:
            logger.info(
                f"Alpaca: Attempting to place {side} order for {qty} of "
                f"{symbol}..."
            )
            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type=type,
                time_in_force=time_in_force
            )
            logger.info(
                f"Alpaca: Placed {side} order for {qty} of {symbol}. "
                f"Order ID: {order.id}"
            )
            return order
        except Exception as e:
            logger.error(f"Alpaca: Error placing order for {symbol}: {e}")
            return None

    async def get_position(self, symbol: str):
        """
        Checks the current position for a given symbol.

        Args:
            symbol (str): The trading symbol.

        Returns:
            Position: The position object if found, None otherwise.
        """
        try:
            logger.info(f"Alpaca: Checking position for {symbol}...")
            position = self.api.get_position(symbol)
            logger.info(
                f"Alpaca: Current position for {symbol}: {position.qty} shares, "
                f"avg price {position.avg_entry_price}"
            )
            return position
        except Exception as e:
            logger.info(f"Alpaca: No position found for {symbol} or error: {e}")
            return None

    async def get_account_info(self):
        """
        Retrieves account information.
        """
        try:
            logger.info("Alpaca: Fetching account information...")
            account = self.api.get_account()
            logger.info(
                f"Alpaca: Account Status: {account.status}, Equity: {account.equity}, "
                f"Buying Power: {account.buying_power}"
            )
            return account
        except Exception as e:
            logger.error(f"Alpaca: Error getting account info: {e}")
            return None
