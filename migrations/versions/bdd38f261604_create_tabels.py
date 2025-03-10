"""Create tabels

Revision ID: bdd38f261604
Revises: 
Create Date: 2025-02-09 10:47:36.522606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdd38f261604'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'carts', 'goods', ['good_id'], ['id'], ondelete='CASCADE')
    op.alter_column('users', 'full_name',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'full_name',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.drop_constraint(None, 'carts', type_='foreignkey')
    # ### end Alembic commands ###
