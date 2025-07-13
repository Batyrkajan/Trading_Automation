## Goal: Transform the Trading Bot into a Backend Service

**Objective:** Refactor the existing trading bot script into a scalable backend service using FastAPI. This will enable a frontend application to consume the bot's data and signals.

--- 

### Active Tasks

- **Task 1: Setup FastAPI and Project Structure**
    - Add `fastapi` and `uvicorn` to `requirements.txt`.
    - Create a new `api` directory within the `app` directory.
    - Initialize a FastAPI app in `app/api/main.py`.

- **Task 2: Create API Endpoints**
    - **`/signal`**: Create a GET endpoint that returns the latest trading signal.
    - **`/state`**: Create a GET endpoint that returns the current state of the bot (last signal, indicators, etc.).
    - **`/history`**: Create a GET endpoint to provide historical indicator data.

- **Task 3: Refactor the Main Loop**
    - Adapt the existing `main.py` logic to run as a background task within the FastAPI application.
    - Ensure the trading loop continues to run independently while the API serves requests.

- **Task 4: Frontend Integration Plan**
    - Document the API endpoints and their expected request/response formats.
    - Create a simple plan for how a frontend application would interact with this backend.

### Backlog

- Implement WebSocket support for real-time updates.
- Add user authentication to protect the API endpoints.
- Develop endpoints for backtesting trading strategies.
- Dockerize the FastAPI application for deployment.
