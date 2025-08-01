from logging.config import fileConfig
import asyncio
import os
from alembic import context

# Load from your app
from db.init_db import engine, Base  # ✅ Reuse these from codebase

# If you use models (optional)
from models import user,exercise  # Import all models so Alembic can see them

# Setup config
config = context.config
fileConfig(config.config_file_name)

# Tell Alembic what metadata to look for
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=os.getenv("URL"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    async def do_run_migrations():
        async with engine.begin() as conn:
            await conn.run_sync(
                lambda sync_conn: context.configure(
                    connection=sync_conn,
                    target_metadata=target_metadata,
                )
            )
            await conn.run_sync(lambda sync_conn: context.run_migrations())
    asyncio.run(do_run_migrations())
	

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
