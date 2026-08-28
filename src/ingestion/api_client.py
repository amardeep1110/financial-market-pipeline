import requests
from config.config import (
    API_KEY,
    INTERVAL,
    OUTPUT_SIZE,
)

BASE_URL = "https://api.twelvedata.com/time_series"


def fetch_market_data(
    symbol,
    interval=INTERVAL,
    outputsize=OUTPUT_SIZE,
):
    """
    Fetch historical market data from Twelve Data.
    """

    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": API_KEY,
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Financial API request timed out."
        )

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Could not connect to the financial API."
        )

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            f"Financial API returned HTTP error: {error}"
        )

    data = response.json()

    # Twelve Data may return an error message
    if "status" in data and data["status"] == "error":
        message = data.get(
            "message",
            "Unknown API error",
        )

        raise RuntimeError(
            f"Twelve Data API error: {message}"
        )

    if "values" not in data:
        raise RuntimeError(
            "API response does not contain market data."
        )

    return data