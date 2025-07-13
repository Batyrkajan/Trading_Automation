from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DEEPSEEK_API_KEY: str
    
    ALPACA_API_KEY: str
    ALPACA_SECRET_KEY: str
    APCA_API_BASE_URL: str = "https://paper-api.alpaca.markets"
    TRADE_ALLOCATION_PERCENTAGE: float = 0.60 # 60% of buying power
    TRADE_INTERVAL_SECONDS: int = 300  # 1 minute interval for trading

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
