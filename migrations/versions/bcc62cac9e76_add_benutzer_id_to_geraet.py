"""Add benutzer_id to Geraet

Revision ID: bcc62cac9e76
Revises: 
Create Date: 2025-04-09 06:32:10.312469
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'bcc62cac9e76'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('geraete', schema=None) as batch_op:
        batch_op.add_column(sa.Column('benutzer_id', sa.Integer(), nullable=True))  # ✅ fix
        batch_op.create_foreign_key(
            constraint_name='fk_geraete_benutzer',
            referent_table='benutzer',
            local_cols=['benutzer_id'],
            remote_cols=['id']
        )

def downgrade():
    with op.batch_alter_table('geraete', schema=None) as batch_op:
        batch_op.drop_constraint('fk_geraete_benutzer', type_='foreignkey')
        batch_op.drop_column('benutzer_id')
