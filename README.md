# Financial Market Data Pipeline

A production-style Python data pipeline for extracting financial market data, cleaning and validating it, calculating technical indicators and risk metrics, and storing the processed data in PostgreSQL.

## Features

* Fetch historical market data from Twelve Data API
* Data cleaning and type conversion using Pandas
* Market data validation
* Daily return calculation
* Moving averages
* Rolling volatility
* Sharpe ratio
* Maximum drawdown
* PostgreSQL data storage
* Database indexing
* Duplicate protection using a unique constraint
* Structured application logging
* API error handling and timeouts
* Automated unit testing with Pytest
* Environment-based configuration
* Automated execution using macOS `launchd`

---

## Project Architecture

```text
                    Twelve Data API
                           │
                           ▼
                    ┌─────────────┐
                    │  Ingestion  │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Cleaning  │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Validation  │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │Transformation│
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Analytics  │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ PostgreSQL  │
                    └─────────────┘
                           │
                           ▼
                    Processed Data
```

---

## Project Structure

```text
financial-market-pipeline/
│
├── config/
│   └── config.py
│
├── src/
│   ├── analytics/
│   │   ├── __init__.py
│   │   └── metrics.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py
│   │   ├── init_db.py
│   │   ├── models.py
│   │   └── repository.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── api_client.py
│   │
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── cleaner.py
│   │   └── validator.py
│   │
│   ├── transformation/
│   │   ├── __init__.py
│   │   └── transformer.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py
│   │
│   └── pipeline.py
│
├── tests/
│   ├── test_cleaner.py
│   ├── test_metrics.py
│   ├── test_transformer.py
│   └── test_validator.py
│
├── logs/
│   └── pipeline.log
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── api_manual_test.py
```

---

## Technologies Used

| Technology      | Purpose                   |
| --------------- | ------------------------- |
| Python          | Pipeline development      |
| Pandas          | Data processing           |
| NumPy           | Numerical calculations    |
| Requests        | API requests              |
| SQLAlchemy      | PostgreSQL interaction    |
| PostgreSQL      | Persistent data storage   |
| Pytest          | Automated testing         |
| python-dotenv   | Environment configuration |
| Twelve Data API | Financial market data     |
| Git/GitHub      | Version control           |
| macOS launchd   | Pipeline scheduling       |

---

## Requirements

* Python 3.9+
* PostgreSQL
* Twelve Data API key
* Git

---

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd financial-market-pipeline
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root.

Use `.env.example` as a template.

```env
TWELVE_DATA_API_KEY=your_api_key_here

DATABASE_URL=postgresql://localhost:5432/market_data

SYMBOL=AAPL
INTERVAL=1day
OUTPUT_SIZE=100
```

### Environment Variables

| Variable              | Description                  | Example                                   |
| --------------------- | ---------------------------- | ----------------------------------------- |
| `TWELVE_DATA_API_KEY` | Twelve Data API key          | `your_api_key_here`                       |
| `DATABASE_URL`        | PostgreSQL connection string | `postgresql://localhost:5432/market_data` |
| `SYMBOL`              | Market symbol                | `AAPL`                                    |
| `INTERVAL`            | Data interval                | `1day`                                    |
| `OUTPUT_SIZE`         | Number of records to fetch   | `100`                                     |

### Security

Never commit `.env` to Git.

The real API key should exist only in:

```text
.env
```

The repository should contain only:

```text
.env.example
```

with a placeholder API key.

---

## PostgreSQL Setup

Create the database:

```bash
createdb market_data
```

Initialize the database tables:

```bash
python -m src.database.init_db
```

The main table is:

```text
market_prices
```

It stores:

* Symbol
* Datetime
* Open
* High
* Low
* Close
* Volume
* Daily return
* 20-day moving average
* 50-day moving average
* 20-day volatility

The database also uses a unique constraint on:

```text
symbol + datetime
```

to prevent duplicate market records.

---

## Running the Pipeline

Run the complete pipeline:

```bash
python -m src.pipeline
```

The pipeline performs:

```text
1. Extract market data
2. Convert API response to DataFrame
3. Clean data
4. Validate data
5. Calculate daily returns
6. Calculate moving averages
7. Calculate volatility
8. Calculate Sharpe ratio
9. Calculate maximum drawdown
10. Save data to PostgreSQL
```

---

## Analytics

### Daily Returns

Daily percentage returns are calculated from consecutive closing prices.

### Moving Averages

The pipeline calculates:

* 20-day moving average
* 50-day moving average

### Volatility

Rolling 20-day volatility is calculated from daily returns.

### Sharpe Ratio

The Sharpe ratio is used to measure risk-adjusted performance.

The implementation annualizes the ratio using 252 trading days.

### Maximum Drawdown

Maximum drawdown measures the largest decline from a historical peak.

---

## Data Validation

Before transformation, market data is validated.

The pipeline checks:

```text
Required columns exist
        ↓
No missing values
        ↓
Prices > 0
        ↓
Volume >= 0
        ↓
High >= Open
High >= Close
        ↓
Low <= Open
Low <= Close
```

Invalid data causes the pipeline to stop rather than storing corrupted records.

---

## Logging

The pipeline uses Python's `logging` module.

Logs are written to:

```text
logs/pipeline.log
```

The application records:

* Pipeline start
* API extraction
* Number of records received
* Cleaning results
* Validation status
* Analytics results
* Database operations
* Pipeline completion
* Exceptions and tracebacks

---

## Testing

Run the complete test suite:

```bash
python -m pytest -v
```

Current tests cover:

```text
Data cleaning
Daily return calculation
Sharpe ratio
Maximum drawdown
Market data validation
```

The project currently contains:

```text
6 tests
```

External API calls are not required for the unit tests.

For manual API testing, use:

```bash
python api_manual_test.py
```

---

## Automated Scheduling

The pipeline can be scheduled on macOS using `launchd`.

The scheduler executes:

```bash
python -m src.pipeline
```

at a configured interval.

Scheduler logs are written to:

```text
logs/launchd.log
logs/launchd-error.log
```

---

## Database Query Examples

Check the number of stored records:

```sql
SELECT COUNT(*)
FROM market_prices;
```

Retrieve recent AAPL data:

```sql
SELECT
    symbol,
    datetime,
    open,
    high,
    low,
    close,
    volume
FROM market_prices
WHERE symbol = 'AAPL'
ORDER BY datetime DESC
LIMIT 10;
```

Retrieve calculated metrics:

```sql
SELECT
    symbol,
    datetime,
    close,
    daily_return,
    ma_20,
    ma_50,
    volatility_20
FROM market_prices
WHERE symbol = 'AAPL'
ORDER BY datetime DESC
LIMIT 10;
```

---

## Example Pipeline Flow

```text
AAPL
 │
 ▼
Twelve Data API
 │
 ▼
100 historical records
 │
 ▼
Pandas DataFrame
 │
 ▼
Data Cleaning
 │
 ▼
Data Validation
 │
 ▼
Technical Indicators
 │
 ├── Daily Returns
 ├── MA20
 ├── MA50
 └── Volatility
 │
 ▼
Risk Analytics
 │
 ├── Sharpe Ratio
 └── Maximum Drawdown
 │
 ▼
PostgreSQL
```

---

## Future Improvements

Planned improvements include:

* Support for multiple symbols
* Incremental data fetching
* Retry mechanism with exponential backoff
* API rate-limit handling
* Better database connection pooling
* Docker support
* CI/CD with GitHub Actions
* Data quality monitoring
* Additional technical indicators
* REST API for querying stored market data
* Dashboard for market analytics
* Backtesting module
* Cloud deployment

---

## Author

**Amardeep Kumar Yadav**

B.Tech — Computer Science Engineering

---

## License

This project is intended for educational and portfolio purposes.
