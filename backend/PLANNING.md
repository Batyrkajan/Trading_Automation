## Project Plan: Trading Bot Backend API

### 1. Objective

Transform the current standalone trading bot script into a robust and scalable backend service using the FastAPI framework. The primary goal is to expose the bot's functionality through a REST API, allowing a frontend application to interact with it for displaying data and trading signals.

### 2. Core Technologies

- **Backend Framework:** FastAPI
- **Web Server:** Uvicorn
- **Existing Stack:** `httpx`, `pydantic`, `yfinance`, `pandas-ta`, `alpaca-trade-api`

### 3. Architecture

The backend will be a single FastAPI application with two main components:

1.  **API Layer:** A set of RESTful endpoints that provide access to the bot's data and signals. This will be the primary interface for the frontend.
2.  **Trading Engine (Background Task):** The existing trading loop will be refactored to run as a background task within the FastAPI application's lifecycle. This ensures that the bot continues to trade autonomously while the API serves requests.

### 4. API Endpoints

The following endpoints will be created:

- `GET /api/signal`
    - **Purpose:** Provide the most recent trading signal (`buy`, `sell`, `hold`).
    - **Response:** A JSON object containing the signal.

- `GET /api/state`
    - **Purpose:** Get the full current state of the bot.
    - **Response:** A JSON object including the last executed signal, the last set of indicators, the last price, and the timestamp of the last update.

- `GET /api/history`
    - **Purpose:** Retrieve historical data for technical indicators.
    - **Response:** A JSON array of historical data points (e.g., timestamp, value) for a specified indicator.

### 5. Development Phases

- **Phase 1: Setup and Refactoring**
    - Integrate FastAPI and Uvicorn into the project.
    - Restructure the project to accommodate the new API layer.
    - Refactor the main trading loop to run as a background process managed by FastAPI.

- **Phase 2: API Implementation**
    - Develop and test the API endpoints defined above.
    - Implement Pydantic models for API request and response validation.

- **Phase 3: Frontend Integration Preparation**
    - Create clear documentation for the API, including endpoint details and example responses.
    - Ensure the API provides all necessary data for a frontend dashboard.

### 6. Future Enhancements (Post-MVP)

- **WebSockets:** Implement a WebSocket connection for pushing real-time updates to the frontend.
- **Authentication:** Secure the API with a token-based authentication system.
- **Database Integration:** Replace the `state.json` file with a proper database (e.g., PostgreSQL) for more robust state and history management.
- **Deployment:** Dockerize the application for easy deployment to a cloud service.