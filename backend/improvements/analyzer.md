🩻 Potential Improvements

1️⃣ Timeouts:
Add request timeouts for reliability:

async with httpx.AsyncClient(timeout=10) as client:
    ...
2️⃣ Retries on transient network errors:
Optionally wrap with retry logic or use httpx built-in retry via httpcore if transient failures are an issue.

3️⃣ Prompt clarity:
Add a testable prompt template in a constants file to centralize prompt logic for version control if prompt engineering evolves.

4️⃣ Unit tests coverage:
Write tests covering:

Successful buy, sell, hold.
Invalid signal returned by DeepSeek.
Network failure.
HTTP failure.
Malformed JSON response.
5️⃣ Rate limiting awareness:
If DeepSeek has rate limits, consider:

Exponential backoff.
Rate limit error type in DeepSeekErrorResponse.
6️⃣ Configurable DeepSeek URL via environment:
Move deepseek_api_url to config for flexibility across environments.