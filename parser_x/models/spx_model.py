from sqlalchemy import (
    Float,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import Base


class SpimexTradingResut(Base):
    __tablename__ = "spimex_trading_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exchange_product_id: Mapped[str] = mapped_column(String, nullable=False)
    exchange_product_name: Mapped[str] = mapped_column(String, nullable=False)
    oil_id: Mapped[str] = mapped_column(String(4), nullable=False)
    delivery_basis_id: Mapped[str] = mapped_column(String(3), nullable=False)
    delivery_basis_name: Mapped[str] = mapped_column(String, nullable=False)
    delivery_type_id: Mapped[str] = mapped_column(String(1), nullable=False)
    volume: Mapped[float] = mapped_column(Float, nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[str] = mapped_column(String, nullable=False)
    created_on: Mapped[str] = mapped_column(String, nullable=False)
    updated_on: Mapped[str] = mapped_column(String, nullable=False)