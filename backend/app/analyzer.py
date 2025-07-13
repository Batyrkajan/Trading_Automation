import httpx
from pydantic import ValidationError
from typing import Union

from app.models import (
    DeepSeekRequest,
    DeepSeekMessage,
    DeepSeekResponse,
    DeepSeekErrorResponse,
)
from app.utils import logger


async def get_trading_signal(
    indicators: dict,
    api_key: str,
) -> Union[str, DeepSeekErrorResponse]:
    """
    Generates a trading signal (buy, sell, or hold) using the DeepSeek API
    based on the provided technical indicators.

    Args:
        indicators (dict): A dictionary of technical indicators.
        api_key: str): Your DeepSeek API key.

    Returns:
        Union[str, DeepSeekErrorResponse]: The trading signal ("buy", "sell",
                                          "hold") or an error response.
    """
    deepseek_api_url = "https://api.deepseek.com/chat/completions"

    prompt_content = (
        f"Given the following technical indicator values:\n"
        f"{indicators}\n\n"
        f"Based on these values, provide a trading signal. Respond with only"
        f" one word: 'buy, sell', or 'hold'."
    )



    messages = [
        DeepSeekMessage(
            role="system",
            content="You are a trading signal generator. Your only output is"
            " 'buy, 'sell', or 'hold'.",
        ),
        DeepSeekMessage(role="user", content=prompt_content),
    ]

    request_body = DeepSeekRequest(messages=messages).model_dump_json(by_alias=True)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    try:
        logger.info("Requesting trading signal from DeepSeek API...")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                deepseek_api_url, headers=headers, content=request_body
            )
            response.raise_for_status()
            data = response.json()

        try:
            deepseek_response = DeepSeekResponse(**data)
            if deepseek_response.choices and \
               deepseek_response.choices[0].message.content:
                signal = (
                    deepseek_response.choices[0].message.content.strip().lower()
                )
                if signal in ["buy", "sell", "hold"]:
                    logger.info(f"Received signal from DeepSeek: {signal}")
                    return signal
                else:
                    logger.warning(
                        f"DeepSeek returned an unexpected signal format: {signal}"
                    )
                    return DeepSeekErrorResponse(
                        error={
                            "message": f"Unexpected signal format: {signal}",
                            "type": "parsing_error",
                        }
                    )
            else:
                logger.warning("No signal found in DeepSeek response.")
                return DeepSeekErrorResponse(
                    error={
                        "message": "No signal found in DeepSeek response.",
                        "type": "parsing_error",
                    }
                )
        except ValidationError as e:
            logger.error(f"Validation error parsing DeepSeek response: {e}")
            try:
                return DeepSeekErrorResponse(**data)
            except ValidationError:
                return DeepSeekErrorResponse(
                    error={
                        "message": f"Failed to parse DeepSeek response: {data}",
                        "type": "validation_error",
                    }
                )

    except httpx.RequestError as exc:
        logger.error(f"Network error during DeepSeek API call: {exc}")
        return DeepSeekErrorResponse(
            error={
                "message": f"Network error during DeepSeek API call: {exc}",
                "type": "network_error",
            }
        )
    except httpx.HTTPStatusError as exc:
        logger.error(
            f"HTTP error from DeepSeek API: {exc.response.status_code} - "
            f"{exc.response.text}"
        )
        return DeepSeekErrorResponse(
            error={
                "message": (
                    f"HTTP error from DeepSeek API: {exc.response.status_code} - "
                    f"{exc.response.text}"
                ),
                "type": "http_error",
            }
        )
    except Exception as exc:
        logger.error(f"An unexpected error occurred during DeepSeek API call: {exc}")
        return DeepSeekErrorResponse(
            error={
                "message": (
                    f"An unexpected error occurred during DeepSeek API call: {exc}"
                ),
                "type": "unexpected_error",
            }
        )
