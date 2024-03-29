"""empty message

Revision ID: 6bdfc6142f93
Revises: 7f13e4b9e697
Create Date: 2024-01-07 16:52:09.639911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bdfc6142f93'
down_revision = '7f13e4b9e697'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lesson', schema=None) as batch_op:
        batch_op.alter_column('iframeCode',
               existing_type=sa.TEXT(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lesson', schema=None) as batch_op:
        batch_op.alter_column('iframeCode',
               existing_type=sa.TEXT(),
               nullable=False)

    # ### end Alembic commands ###
