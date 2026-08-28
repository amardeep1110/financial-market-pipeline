from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Index,
    Integer,
    String,
    UniqueConstraint,
)

from sqlalchemy.orm import declarative_base


Base = declarative_base()


class MarketPrice(Base):
    __tablename__ = "market_prices"

    __table_args__ = (
        UniqueConstraint(
            "symbol",
            "datetime",
            name="uq_market_symbol_datetime",
        ),
        Index(
            "idx_market_symbol_datetime",
            "symbol",
            "datetime",
        ),
    )

    id = Column(Integer, primary_key=True)

    symbol = Column(String(20), nullable=False)
    datetime = Column(DateTime, nullable=False)

    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)

    volume = Column(Float, nullable=False)

    daily_return = Column(Float)
    ma_20 = Column(Float)
    ma_50 = Column(Float)
    volatility_20 = Column(Float)