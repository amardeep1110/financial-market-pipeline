
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
from src.strategy.moving_average import moving_average_crossover
from src.backtesting.performance import calculate_performance_summary
from src.backtesting.trades import generate_trade_log
from src.backtesting.risk import calculate_portfolio_value


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Financial Market Dashboard",
    page_icon="📈",
    layout="wide",
)


# ==================================================
# LOAD MARKET DATA
# ==================================================

@st.cache_data
def load_market_data(symbol):
    return get_market_data(engine, symbol)


# ==================================================
# HEADER
# ==================================================

st.title("📈 Financial Market Dashboard")

st.caption(
    "Financial analytics, PostgreSQL storage and "
    "Moving Average Crossover backtesting."
)


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("Configuration")

symbol = st.sidebar.text_input(
    "Stock Symbol",
    value="AAPL",
).strip().upper()


# ==================================================
# REFRESH DATA
# ==================================================

if st.sidebar.button("🔄 Refresh Data"):

    with st.spinner(
        f"Fetching latest {symbol} data..."
    ):

        try:

            run_pipeline(symbol)

            load_market_data.clear()

            st.success("Market data refreshed.")

            st.rerun()

        except Exception as error:

            st.error(str(error))


# ==================================================
# LOAD DATA
# ==================================================

df = load_market_data(symbol)

if df.empty:

    st.warning(
        f"No data found for {symbol}."
    )

    st.stop()


df["datetime"] = pd.to_datetime(
    df["datetime"]
)

df = (
    df
    .sort_values("datetime")
    .reset_index(drop=True)
)


# ==================================================
# DATE FILTER
# ==================================================

st.sidebar.subheader("Date Range")

min_date = df["datetime"].min().date()
max_date = df["datetime"].max().date()

start_date = st.sidebar.date_input(
    "Start Date",
    min_value=min_date,
    max_value=max_date,
    value=min_date,
)

end_date = st.sidebar.date_input(
    "End Date",
    min_value=min_date,
    max_value=max_date,
    value=max_date,
)


if start_date > end_date:

    st.error("Invalid date range.")

    st.stop()


filtered_df = df[
    (df["datetime"].dt.date >= start_date)
    & (df["datetime"].dt.date <= end_date)
].copy()


if filtered_df.empty:

    st.warning(
        "No records available."
    )

    st.stop()


# ==================================================
# MARKET ANALYTICS
# ==================================================

latest = filtered_df.iloc[-1]

sharpe_ratio = calculate_sharpe_ratio(
    filtered_df
)

max_drawdown = calculate_max_drawdown(
    filtered_df
)


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


# ==================================================
# MOVING AVERAGE STRATEGY
# ==================================================

st.divider()

st.header(
    "Moving Average Crossover Strategy"
)


c1, c2 = st.columns(2)


short_window = c1.number_input(
    "Short Window",
    min_value=2,
    max_value=100,
    value=20,
)


long_window = c2.number_input(
    "Long Window",
    min_value=3,
    max_value=200,
    value=50,
)


if short_window >= long_window:

    st.error(
        "Short window must be smaller."
    )

    st.stop()


strategy_df = moving_average_crossover(
    filtered_df,
    int(short_window),
    int(long_window),
)


# ==================================================
# PORTFOLIO SETTINGS
# ==================================================

st.subheader("Portfolio Settings")


initial_capital = st.number_input(
    "Initial Capital ($)",
    min_value=1000.0,
    max_value=10_000_000.0,
    value=100_000.0,
    step=5_000.0,
)


allocation_percent = st.slider(
    "Capital Allocation per Trade",
    min_value=10,
    max_value=100,
    value=100,
    step=10,
    format="%d%%",
)


# Convert percentage to decimal.
#
# Example:
# 10%  -> 0.10
# 50%  -> 0.50
# 100% -> 1.00

allocation = allocation_percent / 100


# ==================================================
# PORTFOLIO CALCULATION
# ==================================================

portfolio_df = calculate_portfolio_value(
    strategy_df,
    initial_capital=initial_capital,
    allocation=allocation,
)


# ==================================================
# PORTFOLIO PERFORMANCE
# ==================================================

latest_portfolio_value = (
    portfolio_df[
        "portfolio_value"
    ].iloc[-1]
)


profit_loss = (
    latest_portfolio_value
    - initial_capital
)


portfolio_return = (
    latest_portfolio_value
    / initial_capital
) - 1


st.subheader(
    "💰 Portfolio Performance"
)


p1, p2, p3, p4 = st.columns(4)


p1.metric(
    "Initial Capital",
    f"${initial_capital:,.2f}",
)


p2.metric(
    "Portfolio Value",
    f"${latest_portfolio_value:,.2f}",
)


p3.metric(
    "Profit / Loss",
    f"${profit_loss:,.2f}",
)


p4.metric(
    "Portfolio Return",
    f"{portfolio_return * 100:.2f}%",
)


# ==================================================
# PORTFOLIO DETAILS
# ==================================================

p5, p6, p7 = st.columns(3)


latest_cash = (
    portfolio_df["cash"].iloc[-1]
)


latest_shares = (
    portfolio_df["shares"].iloc[-1]
)


latest_position_value = (
    portfolio_df[
        "position_value"
    ].iloc[-1]
)


p5.metric(
    "Cash",
    f"${latest_cash:,.2f}",
)


p6.metric(
    "Shares",
    f"{latest_shares:,}",
)


p7.metric(
    "Position Value",
    f"${latest_position_value:,.2f}",
)


# ==================================================
# PORTFOLIO EQUITY CURVE
# ==================================================

st.subheader(
    "💰 Portfolio Equity Curve"
)


portfolio_fig = go.Figure()


portfolio_fig.add_trace(
    go.Scatter(
        x=portfolio_df["datetime"],
        y=portfolio_df[
            "portfolio_value"
        ],
        mode="lines",
        name="Portfolio Value",
    )
)


portfolio_fig.add_trace(
    go.Scatter(
        x=portfolio_df["datetime"],
        y=(
            strategy_df["close"]
            / strategy_df["close"].iloc[0]
            * initial_capital
        ),
        mode="lines",
        name="Buy & Hold",
    )
)


portfolio_fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Portfolio Value ($)",
    hovermode="x unified",
)


st.plotly_chart(
    portfolio_fig,
    use_container_width=True,
)


# ==================================================
# STRATEGY METRICS
# ==================================================

strategy_return = (
    strategy_df[
        "cumulative_strategy_return"
    ].iloc[-1]
)


buy_hold_return = (
    strategy_df["close"].iloc[-1]
    / strategy_df["close"].iloc[0]
    - 1
)


# ==================================================
# BUY / SELL EVENTS
# ==================================================

buy_events = strategy_df[
    (strategy_df["signal"] == 1)
    & (
        strategy_df["signal"]
        .shift(1)
        .fillna(0)
        != 1
    )
]


sell_events = strategy_df[
    (strategy_df["signal"] == -1)
    & (
        strategy_df["signal"]
        .shift(1)
        .fillna(0)
        != -1
    )
]


current_position = (
    "LONG"
    if strategy_df[
        "position"
    ].iloc[-1] == 1
    else "CASH"
)


# ==================================================
# STRATEGY METRIC CARDS
# ==================================================

m1, m2, m3, m4 = st.columns(4)


m1.metric(
    "Strategy Return",
    f"{strategy_return * 100:.2f}%",
)


m2.metric(
    "Buy & Hold",
    f"{buy_hold_return * 100:.2f}%",
)


m3.metric(
    "Buy Signals",
    len(buy_events),
)


m4.metric(
    "Current Position",
    current_position,
)


# ==================================================
# CANDLESTICK CHART
# ==================================================

st.subheader(
    f"{symbol} Price & Signals"
)


fig = go.Figure()


# OHLC candles

fig.add_trace(
    go.Candlestick(
        x=strategy_df["datetime"],
        open=strategy_df["open"],
        high=strategy_df["high"],
        low=strategy_df["low"],
        close=strategy_df["close"],
        name="OHLC",
    )
)


# Short moving average

fig.add_trace(
    go.Scatter(
        x=strategy_df["datetime"],
        y=strategy_df["short_ma"],
        mode="lines",
        name=f"{short_window} MA",
    )
)


# Long moving average

fig.add_trace(
    go.Scatter(
        x=strategy_df["datetime"],
        y=strategy_df["long_ma"],
        mode="lines",
        name=f"{long_window} MA",
    )
)


# BUY signals

fig.add_trace(
    go.Scatter(
        x=buy_events["datetime"],
        y=buy_events["close"],
        mode="markers",
        name="BUY",
        marker=dict(
            symbol="triangle-up",
            size=13,
            color="green",
        ),
    )
)


# SELL signals

fig.add_trace(
    go.Scatter(
        x=sell_events["datetime"],
        y=sell_events["close"],
        mode="markers",
        name="SELL",
        marker=dict(
            symbol="triangle-down",
            size=13,
            color="red",
        ),
    )
)


fig.update_layout(
    hovermode="x unified",
    xaxis_rangeslider_visible=False,
    yaxis_title="Price",
)


st.plotly_chart(
    fig,
    use_container_width=True,
)


# ==================================================
# STRATEGY VS BUY & HOLD
# ==================================================

st.subheader(
    "Strategy vs Buy & Hold"
)


performance_fig = go.Figure()


performance_fig.add_trace(
    go.Scatter(
        x=strategy_df["datetime"],
        y=(
            strategy_df[
                "cumulative_strategy_return"
            ] * 100
        ),
        mode="lines",
        name="Strategy",
    )
)


buy_hold_curve = (
    strategy_df["close"]
    / strategy_df["close"].iloc[0]
    - 1
) * 100


performance_fig.add_trace(
    go.Scatter(
        x=strategy_df["datetime"],
        y=buy_hold_curve,
        mode="lines",
        name="Buy & Hold",
    )
)


performance_fig.update_layout(
    hovermode="x unified",
    yaxis_title="Cumulative Return (%)",
)


st.plotly_chart(
    performance_fig,
    use_container_width=True,
)


# ==================================================
# TRADING VOLUME
# ==================================================

st.subheader(
    "Trading Volume"
)


volume_fig = go.Figure()


volume_fig.add_trace(
    go.Bar(
        x=filtered_df["datetime"],
        y=filtered_df["volume"],
        name="Volume",
    )
)


st.plotly_chart(
    volume_fig,
    use_container_width=True,
)


# ==================================================
# DAILY RETURNS
# ==================================================

st.subheader(
    "Daily Returns"
)


returns_fig = go.Figure()


returns_fig.add_trace(
    go.Scatter(
        x=filtered_df["datetime"],
        y=(
            filtered_df["daily_return"]
            * 100
        ),
        mode="lines",
        name="Daily Return",
    )
)


returns_fig.update_layout(
    yaxis_title="Return (%)",
    hovermode="x unified",
)


st.plotly_chart(
    returns_fig,
    use_container_width=True,
)


# ==================================================
# VOLATILITY
# ==================================================

st.subheader(
    "20-Day Volatility"
)


vol_fig = go.Figure()


vol_fig.add_trace(
    go.Scatter(
        x=filtered_df["datetime"],
        y=filtered_df["volatility_20"],
        mode="lines",
        name="Volatility",
    )
)


st.plotly_chart(
    vol_fig,
    use_container_width=True,
)


# ==================================================
# MARKET DATA TABLE
# ==================================================

st.subheader(
    "Market Data"
)


columns = [
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


st.dataframe(
    filtered_df[
        columns
    ].sort_values(
        "datetime",
        ascending=False,
    ),
    use_container_width=True,
)


st.divider()


st.caption(
    f"{len(filtered_df)} records • "
    f"{start_date} → {end_date}"
)


# ==================================================
# BACKTESTING PERFORMANCE
# ==================================================

st.divider()


st.subheader(
    "📊 Backtesting Performance"
)


# ==================================================
# TRANSACTION COST
# ==================================================

transaction_cost = st.slider(
    "Transaction Cost per Trade",
    min_value=0.0,
    max_value=0.01,
    value=0.001,
    step=0.0001,
    format="%.4f",
)


performance = calculate_performance_summary(
    strategy_df,
    transaction_cost=transaction_cost,
)


# ==================================================
# PERFORMANCE METRICS
# ==================================================

p1, p2, p3, p4 = st.columns(4)


p1.metric(
    "Strategy Return After Costs",
    (
        f"{performance['strategy_return_after_costs'] * 100:.2f}%"
    ),
)


p2.metric(
    "Buy & Hold Return",
    (
        f"{performance['buy_and_hold_return'] * 100:.2f}%"
    ),
)


p3.metric(
    "Outperformance",
    (
        f"{performance['outperformance'] * 100:.2f}%"
    ),
)


p4.metric(
    "CAGR",
    f"{performance['cagr'] * 100:.2f}%",
)


p5, p6, p7, p8 = st.columns(4)


p5.metric(
    "Strategy Sharpe",
    f"{performance['sharpe_ratio']:.2f}",
)


p6.metric(
    "Strategy Max Drawdown",
    (
        f"{performance['max_drawdown'] * 100:.2f}%"
    ),
)


p7.metric(
    "Win Rate",
    f"{performance['win_rate'] * 100:.2f}%",
)


p8.metric(
    "Number of Trades",
    str(
        performance[
            "number_of_trades"
        ]
    ),
)

# ==================================================
# STRATEGY EQUITY CURVE
# ==================================================

st.subheader(
    "📈 Strategy Equity Curve"
)

equity_fig = go.Figure()


strategy_equity = (
    1
    + strategy_df[
        "cumulative_strategy_return"
    ]
)


buy_hold_equity = (
    strategy_df["close"]
    / strategy_df["close"].iloc[0]
)


equity_fig.add_trace(
    go.Scatter(
        x=strategy_df["datetime"],
        y=strategy_equity * 100,
        mode="lines",
        name="Moving Average Strategy",
    )
)


equity_fig.add_trace(
    go.Scatter(
        x=strategy_df["datetime"],
        y=buy_hold_equity * 100,
        mode="lines",
        name="Buy & Hold",
    )
)


equity_fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Growth of $100 (%)",
    hovermode="x unified",
)


st.plotly_chart(
    equity_fig,
    use_container_width=True,
)

# ==================================================
# PERFORMANCE SUMMARY TABLE
# ==================================================

st.subheader(
    "📋 Performance Summary"
)


summary_df = pd.DataFrame(
    {
        "Metric": [
            "Strategy Return",
            "Strategy Return After Costs",
            "Buy & Hold Return",
            "Outperformance",
            "CAGR",
            "Sharpe Ratio",
            "Maximum Drawdown",
            "Win Rate",
            "Number of Trades",
        ],
        "Value": [
            (
                f"{performance['strategy_return'] * 100:.2f}%"
            ),
            (
                f"{performance['strategy_return_after_costs'] * 100:.2f}%"
            ),
            (
                f"{performance['buy_and_hold_return'] * 100:.2f}%"
            ),
            (
                f"{performance['outperformance'] * 100:.2f}%"
            ),
            (
                f"{performance['cagr'] * 100:.2f}%"
            ),
            (
                f"{performance['sharpe_ratio']:.2f}"
            ),
            (
                f"{performance['max_drawdown'] * 100:.2f}%"
            ),
            (
                f"{performance['win_rate'] * 100:.2f}%"
            ),
            str(
                performance[
                    "number_of_trades"
                ]
            ),
        ],
    }
)


st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True,
)


# ==================================================
# TRADE LOG
# ==================================================

st.divider()


st.subheader(
    "📋 Trade Log"
)


trade_log = generate_trade_log(
    strategy_df
)


if trade_log.empty:

    st.info(
        "No completed trades found "
        "for the selected period."
    )

else:

    st.dataframe(
        trade_log,
        use_container_width=True,
        hide_index=True,
    )
