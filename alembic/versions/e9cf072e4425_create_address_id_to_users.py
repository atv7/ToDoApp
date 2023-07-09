"""create address_id to users

Revision ID: e9cf072e4425
Revises: 0a192b9cadb4
Create Date: 2023-07-03 17:24:42.943168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9cf072e4425'
down_revision = '0a192b9cadb4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("address_id", sa.Integer, nullable=True))
    op.create_foreign_key("address_user_fk", source_table="users", referent_table="address", local_cols=[
                          "address_id"], remote_cols=["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("address_user_fk", table_name="users")
    op.drop_column("users", "address_id")
