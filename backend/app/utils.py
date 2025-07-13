import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
        # logging.FileHandler('trading_board.log')
    ]
)

# Get a logger instance
logger = logging.getLogger(__name__)
