"""add company

Revision ID: f105bf58ecfc
Revises: 5c89a726934c
Create Date: 2026-02-22 13:24:29.435660

"""
from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy


# revision identifiers, used by Alembic.
revision = 'f105bf58ecfc'
down_revision = '5c89a726934c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "company",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("created", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("deleted", sa.DateTime(), nullable=True),
    )

    op.execute("INSERT INTO company (name) VALUES ('株式会社ABC');")
    op.execute("INSERT INTO company (name) VALUES ('DEF株式会社');")
    op.execute("INSERT INTO company (name) VALUES ('ZXE合同会社');")

def downgrade():
    op.drop_table("company")