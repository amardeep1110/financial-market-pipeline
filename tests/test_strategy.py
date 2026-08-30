import pandas as pd
import pytest

from src.strategy.moving_average import moving_average_crossover


def create_test_data():
    """Create predictable market data for testing."""

    return pd.DataFrame(
        {
            "datetime": pd.date_range(
                "2025-01-01",
                periods=60,
                freq="D",
            ),
            "close": list(range(1, 61)),
        }
    )


def test_moving_average_crossover_creates_ma_columns():
    df = create_test_data()

    result = moving_average_crossover(
        df,
        short_window=5,
        long_window=10,
    )

    assert "short_ma" in result.columns
    assert "long_ma" in result.columns


def test_moving_average_crossover_creates_signal():
    df = create_test_data()

    result = moving_average_crossover(
        df,
        short_window=5,
        long_window=10,
    )

    assert "signal" in result.columns
    assert set(result["signal"].unique()).issubset(
        {-1, 0, 1}
    )


def test_position_is_shifted():
    df = create_test_data()

    result = moving_average_crossover(
        df,
        short_window=5,
        long_window=10,
    )

    signal_index = result["signal"].first_valid_index()

    if signal_index is not None and signal_index > 0:
        assert (
            result.loc[signal_index, "position"]
            == result.loc[signal_index - 1, "signal"]
        )


def test_strategy_return_is_calculated():
    df = create_test_data()

    result = moving_average_crossover(
        df,
        short_window=5,
        long_window=10,
    )

    assert "strategy_return" in result.columns


def test_cumulative_strategy_return_is_calculated():
    df = create_test_data()

    result = moving_average_crossover(
        df,
        short_window=5,
        long_window=10,
    )

    assert "cumulative_strategy_return" in result.columns

    assert pd.api.types.is_numeric_dtype(
        result["cumulative_strategy_return"]
    )


def test_invalid_windows_raise_error():
    df = create_test_data()

    with pytest.raises(ValueError):
        moving_average_crossover(
            df,
            short_window=50,
            long_window=20,
        )


def test_missing_close_column_raises_error():
    df = pd.DataFrame(
        {
            "datetime": pd.date_range(
                "2025-01-01",
                periods=10,
                freq="D",
            )
        }
    )

    with pytest.raises(ValueError):
        moving_average_crossover(
            df,
            short_window=3,
            long_window=5,
        )