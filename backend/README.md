# AI Trading Bot

## 🪐 Overview

This project is an AI-powered trading bot in Python designed to automate trading decisions. It retrieves real-time market data, calculates technical indicators, analyzes them using the DeepSeek API, applies a "think twice" logic layer, and executes trades via the Alpaca API.

### Who is it for?

Solo traders, systematic traders, and builders looking for a modular, auditable, and Python-based automated trading system.

### What does it do?

- Automates real-time data fetching and indicator calculation.
- Makes AI-informed trading decisions using a large language model.
- Executes trades with deliberate reasoning checks to prevent errors.
- Manages state to maintain context between trading intervals.

## 🚀 Features

- Fetches real-time cryptocurrency data (`yfinance`).
- Calculates a wide range of technical indicators (`pandas-ta`).
- Generates "buy," "sell," or "hold" signals using the DeepSeek API.
- "Think Twice" logic to avoid redundant trades and trade during low volatility.
- Executes live or paper trades via the Alpaca API.
- Dynamic position sizing based on a percentage of available cash.
- Configurable trading interval.
- Modular, clean, and testable architecture.

## 🛠️ Tech Stack

- **Language:** Python 3.12+
- **HTTP Client:** `httpx`
- **Data Validation:** `pydantic`
- **Financial Data:** `yfinance`, `pandas-ta`
- **Trading:** `alpaca-trade-api`
- **AI Analysis:** DeepSeek API
- **Configuration:** `pydantic-settings`
- **Testing:** `pytest`, `pytest-asyncio`

## ⚙️ Setup

1️⃣ **Clone the repository:**
```bash
git clone <repo-url>
cd backend
```

2️⃣ **Create and activate a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3️⃣ **Install dependencies:**
```bash
pip install -r requirements.txt
```

4️⃣ **Create a `.env` file** in the root directory and add your API keys:

```env
DEEPSEEK_API_KEY="your_deepseek_api_key"

# Alpaca API Credentials
ALPACA_API_KEY="your_alpaca_api_key"
ALPACA_SECRET_KEY="your_alpaca_secret_key"

# Set to the paper trading URL for testing
APCA_API_BASE_URL="https://paper-api.alpaca.markets"
```

5️⃣ **Run the bot:**
```bash
python app/main.py
```

## 🧪 Testing

Run the full suite of unit tests:
```bash
pytest
```

## 🗂️ Project Structure

```
backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py             # Main application loop
│   ├── config.py           # Environment and settings management
│   ├── data_fetcher.py     # Fetches market data and calculates indicators
│   ├── analyzer.py         # Generates trading signals via DeepSeek API
│   ├── thinker.py          # "Think Twice" decision logic
│   ├── trader.py           # Alpaca API integration for trade execution
│   ├── models.py           # Pydantic models for API requests/responses
│   ├── state.py            # Saves and loads bot state
│   └── utils.py            # Utility functions (e.g., logging)
│
├── tests/                  # Unit tests for all modules
├── .env                    # (Create this) API keys and secrets
├── requirements.txt        # Project dependencies
├── README.md               # This file
├── PLANNING.md             # Project planning and architecture
├── TASK.md                 # Task list and backlog
└── PROGRESS_REPORT.md      # Progress reports
```
