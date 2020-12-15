"""empty message

Revision ID: 32e911572a0f
Revises: 13bd0e73ae48
Create Date: 2020-12-03 17:46:05.962462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32e911572a0f'
down_revision = '13bd0e73ae48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.add_column('Artist', sa.Column(
        'seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column(
        'genres', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column(
        'seeking_talent', sa.Boolean(), nullable=True))

    op.execute(
        'UPDATE "Artist" SET seeking_venue = False WHERE seeking_venue IS NULL')
    op.execute(
        'UPDATE "Venue" SET seeking_talent = False WHERE seeking_talent IS NULL')
    op.execute('UPDATE "Venue" SET genres = False WHERE genres IS NULL')
    op.execute(
        'UPDATE "Venue" SET seeking_talent = False WHERE seeking_talent IS NULL')

    op.alter_column('Artist', 'seeking_venue', nullable=False)
    op.alter_column('Venue', 'seeking_talent', nullable=False)
    op.alter_column('Venue', 'genres', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'seeking_description')
    op.drop_column('Venue', 'genres')
    op.drop_column('Artist', 'seeking_venue')
    op.drop_column('Artist', 'seeking_description')
    # ### end Alembic commands ###