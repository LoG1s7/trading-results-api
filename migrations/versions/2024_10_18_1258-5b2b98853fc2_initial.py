"""initial.

Revision ID: 5b2b98853fc2
Revises:
Create Date: 2024-10-18 12:58:43.952552

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5b2b98853fc2"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "spimex_trading_results",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("exchange_product_id", sa.String(), nullable=False),
        sa.Column("exchange_product_name", sa.String(), nullable=False),
        sa.Column("oil_id", sa.String(), nullable=False),
        sa.Column("delivery_basis_id", sa.String(), nullable=False),
        sa.Column("delivery_basis_name", sa.String(), nullable=False),
        sa.Column("delivery_type_id", sa.String(), nullable=False),
        sa.Column("volume", sa.Float(), nullable=False),
        sa.Column("total", sa.Float(), nullable=False),
        sa.Column("count", sa.Float(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column(
            "created_on",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_on",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("spimex_trading_results")
    # ### end Alembic commands ###
