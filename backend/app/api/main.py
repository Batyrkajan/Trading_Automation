import asyncio
from fastapi import FastAPI
from app.state import load_state
from app.background import trading_loop

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(trading_loop())

@app.get("/")
def read_root():
    return {"message": "AI Trading Bot API is running."}

@app.get("/api/signal")
def get_signal():
    last_executed_signal, _ = load_state()
    return {"signal": last_executed_signal}

@app.get("/api/state")
def get_state():
    last_executed_signal, last_indicators = load_state()
    return {
        "last_executed_signal": last_executed_signal,
        "last_indicators": last_indicators,
    }
