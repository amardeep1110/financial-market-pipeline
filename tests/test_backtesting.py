import pandas as pd

from src.backtesting.performance import (
    calculate_buy_and_hold_return,
    calculate_cagr,
    calculate_number_of_trades,
    calculate_performance_summary,
    calculate_strategy_max_drawdown,
    calculate_strategy_return,
    calculate_strategy_sharpe_ratio,
    calculate_win_rate,
)


def test_buy_and_hold_return():

    df = pd.DataFrame(
        {
            "close": [100, 110, 120],
        }
    )

    result = calculate_buy_and_hold_return(df)

    assert round(result, 2) == 0.20


def test_strategy_return():

    df = pd.DataFrame(
        {
            "strategy_return": [
                0.10,
                0.10,
            ]
        }
    )

    result = calculate_strategy_return(df)

    assert round(result, 4) == 0.21


def test_performance_summary():

    df = pd.DataFrame(
        {
            "datetime": pd.date_range(
                "2025-01-01",
                periods=3,
                freq="D",
            ),
            "close": [100, 110, 120],
            "strategy_return": [
                0.05,
                0.05,
                0.05,
            ],
            "position": [
                0,
                1,
                1,
            ],
        }
    )

    result = calculate_performance_summary(df)

    assert "strategy_return" in result
    assert "strategy_return_after_costs" in result
    assert "buy_and_hold_return" in result
    assert "outperformance" in result
    assert "cagr" in result
    assert "sharpe_ratio" in result
    assert "max_drawdown" in result
    assert "win_rate" in result
    assert "number_of_trades" in result

    assert result["strategy_return"] > 0
    assert result["buy_and_hold_return"] > 0
    assert result["win_rate"] == 1.0
    assert result["number_of_trades"] == 1


def test_calculate_cagr():

    df = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                [
                    "2020-01-01",
                    "2021-01-01",
                    "2022-01-01",
                ]
            ),
            "strategy_return": [
                0.10,
                0.10,
                0.10,
            ],
        }
    )

    result = calculate_cagr(df)

    assert result > 0


def test_strategy_sharpe_ratio():

    df = pd.DataFrame(
        {
            "strategy_return": [
                0.01,
                0.02,
                -0.01,
                0.03,
                0.01,
            ]
        }
    )

    result = calculate_strategy_sharpe_ratio(df)

    assert isinstance(result, float)


def test_strategy_max_drawdown():

    df = pd.DataFrame(
        {
            "strategy_return": [
                0.10,
                0.10,
                -0.20,
                0.05,
            ]
        }
    )

    result = calculate_strategy_max_drawdown(df)

    assert result < 0


def test_win_rate():

    df = pd.DataFrame(
        {
            "strategy_return": [
                0.10,
                -0.05,
                0.02,
                0.03,
            ]
        }
    )

    result = calculate_win_rate(df)

    assert result == 0.75


def test_number_of_trades():

    df = pd.DataFrame(
        {
            "position": [
                0,
                1,
                1,
                -1,
                -1,
                0,
            ]
        }
    )

    result = calculate_number_of_trades(df)

    assert result == 3


def test_transaction_cost():

    df = pd.DataFrame(
        {
            "datetime": pd.date_range(
                "2025-01-01",
                periods=5,
                freq="D",
            ),
            "close": [
                100,
                105,
                110,
                115,
                120,
            ],
            "strategy_return": [
                0.05,
                0.05,
                0.05,
                0.05,
                0.05,
            ],
            "position": [
                0,
                1,
                1,
                -1,
                0,
            ],
        }
    )

    result = calculate_performance_summary(
        df,
        transaction_cost=0.001,
    )

    assert (
        result["strategy_return_after_costs"]
        < result["strategy_return"]
    )

    
# ==================================================
# Trade Log Tests
# ==================================================

from src.backtesting.trades import generate_trade_log


def test_generate_trade_log():

    df = pd.DataFrame(
        {
            "datetime": pd.date_range(
                "2025-01-01",
                periods=6,
                freq="D",
            ),
            "close": [
                100,
                105,
                110,
                108,
                115,
                120,
            ],
            "position": [
                0,
                1,
                1,
                1,
                0,
                0,
            ],
        }
    )

    result = generate_trade_log(df)

    assert len(result) == 1

    assert result.iloc[0]["entry_price"] == 105

    assert result.iloc[0]["exit_price"] == 115

    assert result.iloc[0]["result"] == "WIN"


def test_open_trade_is_closed_at_last_price():

    df = pd.DataFrame(
        {
            "datetime": pd.date_range(
                "2025-01-01",
                periods=4,
                freq="D",
            ),
            "close": [
                100,
                105,
                110,
                120,
            ],
            "position": [
                0,
                1,
                1,
                1,
            ],
        }
    )

    result = generate_trade_log(df)

    assert len(result) == 1

    assert result.iloc[0]["entry_price"] == 105

    assert result.iloc[0]["exit_price"] == 120

    assert result.iloc[0]["result"] == "WIN"


def test_trade_log_missing_column():

    df = pd.DataFrame(
        {
            "datetime": pd.date_range(
                "2025-01-01",
                periods=3,
                freq="D",
            ),
            "close": [100, 110, 120],
        }
    )

    try:
        generate_trade_log(df)
        assert False
    except ValueError:
        assert True


# ==================================================
# Risk Management Tests
# ==================================================

from src.backtesting.risk import (
    calculate_position_size,
    calculate_position_value,
    calculate_trade_profit_loss,
)


def test_calculate_position_size():

    shares = calculate_position_size(
        capital=10000,
        price=100,
        allocation=1.0,
    )

    assert shares == 100


def test_calculate_position_size_partial_allocation():

    shares = calculate_position_size(
        capital=10000,
        price=100,
        allocation=0.5,
    )

    assert shares == 50


def test_calculate_position_value():

    value = calculate_position_value(
        shares=50,
        price=120,
    )

    assert value == 6000


def test_calculate_trade_profit_loss():

    profit = calculate_trade_profit_loss(
        entry_price=100,
        exit_price=120,
        shares=50,
    )

    assert profit == 1000


# ==================================================
# Portfolio Value Tests
# ==================================================

from src.backtesting.risk import (
    calculate_portfolio_value,
)


def test_calculate_portfolio_value():

    df = pd.DataFrame(
        {
            "close": [
                100,
                110,
                120,
            ],
            "position": [
                0,
                1,
                1,
            ],
        }
    )

    result = calculate_portfolio_value(
        df,
        initial_capital=10000,
        allocation=1.0,
    )

    assert result["portfolio_value"].iloc[0] == 10000

    assert result["portfolio_value"].iloc[-1] == 12000


def test_partial_allocation():

    df = pd.DataFrame(
        {
            "close": [
                100,
                110,
            ],
            "position": [
                0,
                1,
            ],
        }
    )

    result = calculate_portfolio_value(
        df,
        initial_capital=10000,
        allocation=0.5,
    )

    assert result["shares"].iloc[-1] == 50

    assert result["portfolio_value"].iloc[-1] == 10500
