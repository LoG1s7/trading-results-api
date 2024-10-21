from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime, Float, Integer, String, text
from sqlalchemy.orm import mapped_column


def not_nullable_str_with_limit(length: int):
    return Annotated[str, mapped_column(String(length), nullable=False)]


integer_pk = Annotated[
    int, mapped_column(Integer, primary_key=True, autoincrement=True)
]
not_nullable_float = Annotated[float, mapped_column(Float, nullable=False)]

dt_now_utc_sql = text("TIMEZONE('utc', now())")
created_at = Annotated[datetime, mapped_column(DateTime, server_default=dt_now_utc_sql)]
updated_at = Annotated[
    datetime,
    mapped_column(
        DateTime,
        server_default=dt_now_utc_sql,
        onupdate=dt_now_utc_sql,
    ),
]
