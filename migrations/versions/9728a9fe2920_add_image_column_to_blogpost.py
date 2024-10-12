"""Add image column to BlogPost

Revision ID: 9728a9fe2920
Revises: 
Create Date: 2024-10-12 18:49:46.517881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9728a9fe2920'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog_post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(length=120), nullable=True))
        batch_op.alter_column('date_posted',
               existing_type=sa.DATETIME(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog_post', schema=None) as batch_op:
        batch_op.alter_column('date_posted',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.drop_column('image')

    # ### end Alembic commands ###
