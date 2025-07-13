import asyncio
from app.data_fetcher import get_realtime_data, calculate_indicators
from app.analyzer import get_trading_signal
from app.thinker import should_execute_trade
from app.trader import AlpacaTrader
from app.config import settings

from app.utils import logger
from app.state import load_state, save_state


async def main():
    logger.info("Starting the AI Trading Bot...")

    # --- Symbol Configuration ---
    TICKER = "BTC-USD"  # Using yfinance format
    ALPACA_SYMBOL = "BTCUSD"

    trader = AlpacaTrader()
    await trader.get_account_info()

    while True:
        try:
            last_executed_signal, last_indicators = load_state()

            logger.info(f"\n--- Fetching Real-Time Data for {TICKER} ---")
            data = get_realtime_data(TICKER)
            if data.empty:
                logger.warning(f"No real-time data fetched for {TICKER}. Skipping this interval.")
                await asyncio.sleep(settings.TRADE_INTERVAL_SECONDS)
                continue
            
            data = calculate_indicators(data)
            
            if 'close_btc-usd' not in data.columns:
                logger.error(f"'close' column not found in fetched data for {TICKER}. Available columns: {data.columns.tolist()}. Skipping this interval.")
                await asyncio.sleep(settings.TRADE_INTERVAL_SECONDS)
                continue

            current_indicators = data.iloc[-1].to_dict()

            logger.info(f"Current Indicators for {TICKER}:")
            for key, value in current_indicators.items():
                logger.info(f"  {key}: {value}")

            logger.info("\n--- Generating Trading Signal ---")
            proposed_signal = await get_trading_signal(
                indicators=current_indicators,
                api_key=settings.DEEPSEEK_API_KEY
            )

            if isinstance(proposed_signal, str):
                logger.info(f"Proposed Trading Signal: {proposed_signal.upper()}")
            else:
                logger.error(f"Error generating signal: {proposed_signal.error.message}")
                continue

            logger.info("\n--- Applying Thinker Logic ---")
            execute_trade = await should_execute_trade(
                proposed_signal=proposed_signal,
                last_executed_signal=last_executed_signal,
                min_rsi_change_threshold=0.5,  # Enabled this rule
                current_indicators=current_indicators,
                last_indicators=last_indicators
            )

            if execute_trade:
                logger.info("Thinker: Trade approved. Proceeding to execution.")
                position = await trader.get_position(symbol=ALPACA_SYMBOL)

                if proposed_signal == "buy":
                    if position:
                        logger.info("Trader: Position already open. No trade executed.")
                    else:
                        account_info = await trader.get_account_info()
                        if account_info:
                            buying_power = float(account_info.cash)
                            try:
                                logger.info(f"Attempting to get current price from data. Columns: {data.columns.tolist()}")
                                current_price = data.iloc[-1]['close_btc-usd'] # Get current closing price
                                current_timestamp = data.index[-1].timestamp()
                                logger.info(f"Successfully retrieved current price: {current_price}")
                            except Exception as price_e:
                                logger.error(f"Error getting current price: {price_e}, type: {type(price_e)}. Skipping trade for this interval.")
                                continue # Skip this iteration if price cannot be retrieved

                            if current_price > 0:
                                # Calculate quantity based on a percentage of buying power
                                trade_amount = buying_power * settings.TRADE_ALLOCATION_PERCENTAGE
                                trade_qty = trade_amount / current_price # Allow fractional quantities
                                
                                if trade_qty > 0:
                                    await trader.place_order(symbol=ALPACA_SYMBOL, qty=trade_qty, side="buy")
                                else:
                                    logger.info("Calculated trade quantity is zero. Not placing order.")
                            else:
                                logger.error("Current price is zero or negative, cannot calculate trade quantity.")
                        else:
                            logger.error("Could not retrieve account info to determine buying power.")
                elif proposed_signal == "sell":
                    if position:
                        await trader.place_order(symbol=ALPACA_SYMBOL, qty=position.qty, side="sell")
                    else:
                        logger.info("Trader: No position to sell. No trade executed.")
                elif proposed_signal == "hold":
                    logger.info("Trader: Signal is HOLD. No trade executed.")

                await trader.get_position(symbol=ALPACA_SYMBOL)

                last_executed_signal = proposed_signal
                save_state(last_executed_signal, current_indicators, 
                           current_price, 
                           current_timestamp)
            else:
                logger.info("Thinker: Trade not approved. Skipping execution.")

        except Exception as e:
            logger.error(f"An error occurred in the main loop: {e}")

        logger.info(f"\n--- Waiting for the next {settings.TRADE_INTERVAL_SECONDS} seconds interval ---")
        await asyncio.sleep(settings.TRADE_INTERVAL_SECONDS)


if __name__ == "__main__":
    asyncio.run(main())