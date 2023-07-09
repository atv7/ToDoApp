"""create phone number for users col

Revision ID: dd40fdd6a176
Revises: 
Create Date: 2023-07-03 17:09:26.986736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd40fdd6a176'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column(
        "phone_number", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
