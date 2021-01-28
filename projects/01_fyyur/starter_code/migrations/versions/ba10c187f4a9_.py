"""empty message

Revision ID: ba10c187f4a9
Revises: 1aaeb165a5af
Create Date: 2021-01-27 17:25:27.605886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba10c187f4a9'
down_revision = '1aaeb165a5af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('website', sa.String(length=500), nullable=True))
    op.add_column('Venue', sa.Column('website', sa.String(length=500), nullable=True))
    op.drop_column('Venue', 'genres')

    op.execute('UPDATE "Venue" SET website= False WHERE website IS NULL')
    op.execute('UPDATE "Artist" SET website= False WHERE website IS NULL')

    op.alter_column('Venue', 'website', nullable=False)
    op.alter_column('Artist', 'website', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    op.drop_column('Venue', 'website')
    op.drop_column('Artist', 'website')
    # ### end Alembic commands ###
