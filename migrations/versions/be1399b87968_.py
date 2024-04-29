"""empty message

Revision ID: be1399b87968
Revises: 
Create Date: 2024-04-25 19:01:53.378998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be1399b87968'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admindetails',
    sa.Column('USER_ID', sa.String(length=15), nullable=False),
    sa.Column('FIRST_NAME', sa.String(length=150), nullable=False),
    sa.Column('MIDDLE_NAME', sa.String(length=150), nullable=True),
    sa.Column('LAST_NAME', sa.String(length=150), nullable=True),
    sa.Column('EMAIL_ID', sa.String(length=150), nullable=False),
    sa.Column('PASSWORD', sa.String(length=100), nullable=False),
    sa.Column('MOBILE_NUMBER', sa.String(length=150), nullable=True),
    sa.Column('ROLE', sa.String(length=150), nullable=False),
    sa.Column('EFFECTIVE_START_DATE', sa.Date(), nullable=True),
    sa.Column('EFFECTIVE_END_DATE', sa.Date(), nullable=True),
    sa.Column('CREATED_BY', sa.String(length=150), nullable=True),
    sa.Column('LAST_UPDATED_BY', sa.String(length=150), nullable=True),
    sa.Column('CREATION_DATE', sa.DateTime(), nullable=True),
    sa.Column('LAST_UPDATED_DATE', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('USER_ID'),
    sa.UniqueConstraint('EMAIL_ID')
    )
    op.create_table('employeedetails',
    sa.Column('EMPLOYEE_ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('EMPLOYEE_NUMBER', sa.String(length=15), nullable=False),
    sa.Column('WORKER_TYPE', sa.String(length=15), nullable=False),
    sa.Column('FIRST_NAME', sa.String(length=150), nullable=False),
    sa.Column('MIDDLE_NAME', sa.String(length=150), nullable=True),
    sa.Column('LAST_NAME', sa.String(length=150), nullable=False),
    sa.Column('DATE_OF_JOINING', sa.Date(), nullable=False),
    sa.Column('LOCATION', sa.String(length=150), nullable=False),
    sa.Column('EMAIL_ID', sa.String(length=150), nullable=False),
    sa.Column('EFFECTIVE_START_DATE', sa.Date(), nullable=True),
    sa.Column('EFFECTIVE_END_DATE', sa.Date(), nullable=True),
    sa.Column('CREATED_BY', sa.String(length=150), nullable=False),
    sa.Column('LAST_UPDATED_BY', sa.String(length=150), nullable=False),
    sa.Column('CREATION_DATE', sa.DateTime(), nullable=True),
    sa.Column('LAST_UPDATED_DATE', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('EMPLOYEE_ID')
    )
    op.create_table('templatedb',
    sa.Column('TEMPLATE_ID', sa.String(length=15), nullable=False),
    sa.Column('TEMPLATE_NAME', sa.String(length=150), nullable=False),
    sa.Column('TEMPLATE', sa.LargeBinary(length=20971520), nullable=True),
    sa.Column('TEMPLATE_SIZE', sa.Integer(), nullable=True),
    sa.Column('TEMPLATE_TYPE', sa.String(length=150), nullable=True),
    sa.Column('CREATED_BY', sa.String(length=150), nullable=True),
    sa.Column('LAST_UPDATED_BY', sa.String(length=150), nullable=True),
    sa.Column('CREATION_DATE', sa.DateTime(), nullable=True),
    sa.Column('LAST_UPDATED_DATE', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('TEMPLATE_ID')
    )
    op.create_table('addressdetails',
    sa.Column('ADDRESS_ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('EMPLOYEE_ID', sa.Integer(), nullable=True),
    sa.Column('ADDRESS_TYPE', sa.String(length=15), nullable=True),
    sa.Column('ADDRESS', sa.String(length=15), nullable=False),
    sa.Column('CITY', sa.String(length=15), nullable=False),
    sa.Column('STATE', sa.String(length=15), nullable=False),
    sa.Column('COUNTRY', sa.String(length=15), nullable=False),
    sa.Column('PIN_CODE', sa.String(length=15), nullable=False),
    sa.Column('DATE_FROM', sa.Date(), nullable=False),
    sa.Column('DATE_TO', sa.Date(), nullable=True),
    sa.Column('CREATED_BY', sa.String(length=150), nullable=True),
    sa.Column('LAST_UPDATED_BY', sa.String(length=150), nullable=True),
    sa.Column('CREATION_DATE', sa.DateTime(), nullable=True),
    sa.Column('LAST_UPDATED_DATE', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['EMPLOYEE_ID'], ['employeedetails.EMPLOYEE_ID'], ),
    sa.PrimaryKeyConstraint('ADDRESS_ID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('addressdetails')
    op.drop_table('templatedb')
    op.drop_table('employeedetails')
    op.drop_table('admindetails')
    # ### end Alembic commands ###
