from pydantic import BaseModel
from typing import List, Optional, Union


class IndicatorValue(BaseModel):
    value: float


class HistoricalIndicatorDataPoint(BaseModel):
    timestamp: int
    value: float





# DeepSeek API Models
class DeepSeekMessage(BaseModel):
    role: str
    content: str


class DeepSeekRequest(BaseModel):
    model: str = "deepseek-chat"
    messages: List[DeepSeekMessage]
    temperature: float = 0.7
    max_tokens: int = 150
    stream: bool = False


class DeepSeekChoice(BaseModel):
    index: int
    message: DeepSeekMessage
    finish_reason: str


class DeepSeekUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class DeepSeekResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[DeepSeekChoice]
    usage: DeepSeekUsage


class DeepSeekError(BaseModel):
    message: str
    type: str
    param: Optional[str] = None
    code: Optional[str] = None


class DeepSeekErrorResponse(BaseModel):
    error: DeepSeekError



