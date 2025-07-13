import json
from typing import Optional, Tuple

from app.utils import logger

STATE_FILE = "state.json"


def load_state() -> Tuple[Optional[str], Optional[dict]]:
    """
    Loads the last executed signal and indicators from the state file.

    Returns:
        Tuple[Optional[str], Optional[dict]]: A tuple containing the last
                                               executed signal and indicators.
    """
    try:
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
            logger.info(f"Loaded state from {STATE_FILE}: {state}")
            return state.get("last_executed_signal"), state.get("last_indicators")
    except FileNotFoundError:
        logger.info(f"{STATE_FILE} not found. Starting with a clean state.")
        return None, None
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from {STATE_FILE}. Starting fresh.")
        return None, None


def save_state(last_executed_signal: Optional[str], last_indicators: Optional[dict], last_price: Optional[float], last_updated: Optional[int]):
    """
    Saves the last executed signal and indicators to the state file.

    Args:
        last_executed_signal (Optional[str]): The last executed signal.
        last_indicators (Optional[dict]): The last indicators.
    """
    state = {
        "last_executed_signal": last_executed_signal,
        "last_indicators": last_indicators,
        "last_price": last_price,
        "last_updated": last_updated,
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)
    logger.info(f"Saved state to {STATE_FILE}: {state}")