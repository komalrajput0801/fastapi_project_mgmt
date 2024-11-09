"""empty message

Revision ID: 38313e67b98d
Revises: d55deb3cd5d8
Create Date: 2022-12-19 00:20:23.338707

"""
import fastapi_utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38313e67b98d'
down_revision = 'd55deb3cd5d8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
                    sa.Column('id', fastapi_utils.guid_type.GUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=True),
                    sa.Column('owner_id', fastapi_utils.guid_type.GUID(), nullable=True),
                    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('collaborators',
    sa.Column('project_id', fastapi_utils.guid_type.GUID(), nullable=True),
    sa.Column('user_id', fastapi_utils.guid_type.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('collaborators')
    op.drop_table('project')
    # ### end Alembic commands ###
