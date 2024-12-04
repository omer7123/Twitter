"""make image_url not nullable

Revision ID: c115657903e9
Revises: ddd1be2ed175
Create Date: 2024-12-05 02:30:20.840941

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c115657903e9'
down_revision: Union[str, None] = 'ddd1be2ed175'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("UPDATE users SET image_url = '' WHERE image_url IS NULL")
    op.alter_column('users', 'image_url',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'image_url',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###