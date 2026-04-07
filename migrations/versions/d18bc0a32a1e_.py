from alembic import op
import sqlalchemy as sa

revision = 'd18bc0a32a1e'
down_revision = '84b64537781e'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('purchases', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reference', sa.String(length=20), nullable=False))

        batch_op.create_unique_constraint(
            "uq_purchases_reference",
            ['reference']
        )


def downgrade():
    with op.batch_alter_table('purchases', schema=None) as batch_op:
        batch_op.drop_constraint(
            "uq_purchases_reference",
            type_='unique'
        )
        batch_op.drop_column('reference')