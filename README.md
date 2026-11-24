# Price Tracker application for Decathlon UA website 

A Python-based price tracking application that collects product data from Decathlon, stores it in a database, and tracks price changes over time.

The project provides a REST API built with FastAPI and automatically updates product prices every 3 hours.

### Features
- Product scraping — collects product information from Decathlon using its Algolia API.
- Product storage — stores product data in an SQLite database using SQLAlchemy.
- Price history — records price changes over time.
- Duplicate prevention — identifies products using their source and source ID.
- Automatic updates — periodically fetches the latest product prices every 3 hours.
- REST API — provides endpoints to retrieve products and their price history, and trigger scraping manually.
- Automated tests — includes tests for repositories, services, and API endpoints.

### Libraries requirements 
- Python
- FastAPI
- SQLAlchemy 2.0
- SQLite
- Pydantic
- httpx
- APScheduler
- Pytest

### Download and start the application
1. Clone the repository:
```cmd
git clone https://github.com/enderavour/price_tracker.git
cd price_tracker
```
2. Create virtual environment 
```cmd
python -m venv venv
```
3. Activate it:
- Windows:
```cmd
.venv\Scripts\activate
```
- *nix:
```cmd
source .venv/bin/activate
```
4. Install requirements 
```cmd
pip install -r requirements.txt
```
5. Configure environment variables 
Create a .env file based on .env.example and provide the required Decathlon Algolia API credentials.

Steps to extract Algolia API credentials:
- Navigate to the [Decathlon UA](https://www.decathlon.ua/uk/29596-zimovi-kurtki?hpbanner-popular-3) website, open Chrome DevTools. 
- Navigate to Fetch/XHR requests. Update the page, and search request with "queries?x-algolia-agent=..." pattern. 
- Open this request, open "Headers" tab and get the "Request URL" window. Get the URL provided, and get the values from "&x-algolia-application-id=" and "&x-algolia-api-key=". Paste those values into .env.example, and rename it just to .env

6. Run the application:
```cmd
uvicorn app.main:app --reload
```
The application will automatically create the required database tables and start the scheduled price update process.

7. Documentation 
Once the application is running, interactive API documentation is available at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

8. Scheduled updates
The application uses APScheduler to run periodic price updates.
The first update starts when the application starts.
Subsequent updates run every 3 hours.
Price history entries are created only when a product's price changes.

### Running tests 
To run the tests:
```
PYTHONPATH=. pytest -v
```

### Current limitations
- Decathlon is currently the only supported product source.
- Product categories are configured in the application.
- The application currently uses SQLite for data storage.
- There is no frontend interface yet.

### Roadmap of the application
- Support additional online stores.
- Add product search and filtering.
- Add price history visualization.
- Add minimum-price tracking.
- Implement price alerts and notifications.
- Develop a web frontend.
- Add database migrations with Alembic.

### License 
This project is built to the minimal MVP, and is currently still under development. A license will be added before public distribution.