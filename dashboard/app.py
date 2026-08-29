
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.analytics.metrics import (
    calculate_max_drawdown,
    calculate_sharpe_ratio,
)
from src.database.db import engine
from src.database.repository import get_market_data
from src.pipeline import run_pipeline


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Financial Market Dashboard",
    page_icon="📈",
    layout="wide",
)


# --------------------------------------------------
# Load data
# --------------------------------------------------

@st.cache_data
def load_market_data(symbol):
    """Load market data from PostgreSQL."""
    return get_market_data(engine, symbol)


# --------------------------------------------------
# Dashboard title
# --------------------------------------------------

st.title("📈 Financial Market Dashboard")

st.caption(
    "Interactive market analytics powered by "
    "Python, PostgreSQL, Pandas and Plotly."
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Configuration")

symbol = st.sidebar.text_input(
    "Stock Symbol",
    value="AAPL",
).strip().upper()


# --------------------------------------------------
# Refresh button
# --------------------------------------------------

if st.sidebar.button("🔄 Refresh Data"):

    with st.spinner(
        f"Fetching latest {symbol} market data..."
    ):

        try:
            run_pipeline(symbol)

            # Clear cached database data
            load_market_data.clear()

            st.success(
                f"Successfully refreshed {symbol} market data."
            )

            st.rerun()

        except Exception as error:

            st.error(
                f"Failed to refresh market data: {error}"
            )


# --------------------------------------------------
# Load data
# --------------------------------------------------

df = load_market_data(symbol)


if df.empty:

    st.warning(
        f"No market data found for {symbol}. "
        "Run the pipeline first."
    )

    st.stop()


# --------------------------------------------------
# Prepare data
# --------------------------------------------------

df["datetime"] = pd.to_datetime(
    df["datetime"]
)

df = (
    df
    .sort_values("datetime")
    .reset_index(drop=True)
)


# --------------------------------------------------
# Date range filter
# --------------------------------------------------

st.sidebar.subheader("Date Range")

min_date = df["datetime"].min().date()
max_date = df["datetime"].max().date()


start_date = st.sidebar.date_input(
    "Start Date",
    value=min_date,
    min_value=min_date,
    max_value=max_date,
)


end_date = st.sidebar.date_input(
    "End Date",
    value=max_date,
    min_value=min_date,
    max_value=max_date,
)


if start_date > end_date:

    st.error(
        "Start date must be before end date."
    )

    st.stop()


# --------------------------------------------------
# Apply date filter
# --------------------------------------------------

filtered_df = df[
    (df["datetime"].dt.date >= start_date)
    & (df["datetime"].dt.date <= end_date)
].copy()


if filtered_df.empty:

    st.warning(
        "No data available for the selected date range."
    )

    st.stop()


# --------------------------------------------------
# Latest record
# --------------------------------------------------

latest = filtered_df.iloc[-1]


# --------------------------------------------------
# Calculate analytics
# --------------------------------------------------

sharpe_ratio = calculate_sharpe_ratio(
    filtered_df
)

max_drawdown = calculate_max_drawdown(
    filtered_df
)


# --------------------------------------------------
# KPI cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Latest Price",
    f"${latest['close']:.2f}",
)


col2.metric(
    "Daily Return",
    (
        f"{latest['daily_return'] * 100:.2f}%"
        if pd.notna(latest["daily_return"])
        else "N/A"
    ),
)


col3.metric(
    "Sharpe Ratio",
    f"{sharpe_ratio:.2f}",
)


col4.metric(
    "Maximum Drawdown",
    f"{max_drawdown * 100:.2f}%",
)


# --------------------------------------------------
# Candlestick Price Chart
# --------------------------------------------------

st.subheader(
    f"{symbol} Price History"
)


price_fig = go.Figure()


price_fig.add_trace(
    go.Candlestick(
        x=filtered_df["datetime"],
        open=filtered_df["open"],
        high=filtered_df["high"],
        low=filtered_df["low"],
        close=filtered_df["close"],
        name="OHLC",
    )
)


# --------------------------------------------------
# 20-Day Moving Average
# --------------------------------------------------

if "ma_20" in filtered_df.columns:

    price_fig.add_trace(
        go.Scatter(
            x=filtered_df["datetime"],
            y=filtered_df["ma_20"],
            mode="lines",
            name="20-Day MA",
        )
    )


# --------------------------------------------------
# 50-Day Moving Average
# --------------------------------------------------

if "ma_50" in filtered_df.columns:

    price_fig.add_trace(
        go.Scatter(
            x=filtered_df["datetime"],
            y=filtered_df["ma_50"],
            mode="lines",
            name="50-Day MA",
        )
    )


price_fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Price ($)",
    hovermode="x unified",
    xaxis_rangeslider_visible=False,
)


st.plotly_chart(
    price_fig,
    use_container_width=True,
)


# --------------------------------------------------
# Trading Volume
# --------------------------------------------------

st.subheader(
    "Trading Volume"
)


volume_fig = go.Figure()


if "volume" in filtered_df.columns:

    volume_fig.add_trace(
        go.Bar(
            x=filtered_df["datetime"],
            y=filtered_df["volume"],
            name="Volume",
        )
    )


volume_fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Volume",
    hovermode="x unified",
)


st.plotly_chart(
    volume_fig,
    use_container_width=True,
)


# --------------------------------------------------
# Daily Returns
# --------------------------------------------------

st.subheader(
    "Daily Returns"
)


returns_fig = go.Figure()


if "daily_return" in filtered_df.columns:

    returns_fig.add_trace(
        go.Scatter(
            x=filtered_df["datetime"],
            y=filtered_df["daily_return"] * 100,
            mode="lines",
            name="Daily Return",
        )
    )


returns_fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Return (%)",
    hovermode="x unified",
)


st.plotly_chart(
    returns_fig,
    use_container_width=True,
)


# --------------------------------------------------
# 20-Day Volatility
# --------------------------------------------------

st.subheader(
    "20-Day Volatility"
)


volatility_fig = go.Figure()


if "volatility_20" in filtered_df.columns:

    volatility_fig.add_trace(
        go.Scatter(
            x=filtered_df["datetime"],
            y=filtered_df["volatility_20"],
            mode="lines",
            name="20-Day Volatility",
        )
    )


volatility_fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Volatility",
    hovermode="x unified",
)


st.plotly_chart(
    volatility_fig,
    use_container_width=True,
)


# --------------------------------------------------
# Market Data Table
# --------------------------------------------------

st.subheader(
    "Market Data"
)


display_columns = [
    "datetime",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "daily_return",
    "ma_20",
    "ma_50",
    "volatility_20",
]


available_columns = [
    column
    for column in display_columns
    if column in filtered_df.columns
]


st.dataframe(
    filtered_df[
        available_columns
    ].sort_values(
        "datetime",
        ascending=False,
    ),
    use_container_width=True,
)


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()


st.caption(
    f"Showing {len(filtered_df)} records for "
    f"{symbol} from {start_date} to {end_date}."
)
