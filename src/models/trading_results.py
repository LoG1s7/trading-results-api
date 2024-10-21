from datetime import date

from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base
from src.utils.custom_types import (
    created_at,
    integer_pk,
    not_nullable_float,
    not_nullable_str_with_limit,
    updated_at,
)


class SpimexTradingResults(Base):
    __tablename__ = "spimex_trading_results"

    id: Mapped[integer_pk]
    exchange_product_id: Mapped[not_nullable_str_with_limit(20)]
    exchange_product_name: Mapped[not_nullable_str_with_limit(255)]
    oil_id: Mapped[not_nullable_str_with_limit(4)]
    delivery_basis_id: Mapped[not_nullable_str_with_limit(3)]
    delivery_basis_name: Mapped[not_nullable_str_with_limit(255)]
    delivery_type_id: Mapped[not_nullable_str_with_limit(1)]
    volume: Mapped[not_nullable_float]
    total: Mapped[not_nullable_float]
    count: Mapped[not_nullable_float]
    date: Mapped[date] = mapped_column(Date, nullable=False)
    created_on: Mapped[created_at]
    updated_on: Mapped[updated_at]
