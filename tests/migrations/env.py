import os
from dotenv import load_dotenv

import asyncio
from contextvars import ContextVar
from typing import Any

from alembic.runtime.environment import EnvironmentContext
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from logging.config import fileConfig

from sqlalchemy import pool

from alembic import context

from app.entity.base import Base
from app.entity.companies import Company
from app.entity.transaction_statuses import TransactionStatus
from app.entity.currency_types import CurrencyType
from app.entity.customers import Customer
from app.entity.products import Product
from app.entity.transactions import Transaction

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

load_dotenv('.env')
section = config.config_ini_section
config.set_section_option(section, "DATABASE_USER", os.getenv("DATABASE_USER"))
config.set_section_option(section, "DATABASE_HOST",  os.getenv("DATABASE_HOST"))
config.set_section_option(section, "DATABASE_PASSWORD",  os.getenv("DATABASE_PASSWORD"))
config.set_section_option(section, "DATABASE_PORT",  os.getenv("DATABASE_PORT"))
config.set_section_option(section, "DATABASE_DATABASE",  os.getenv("DATABASE_DATABASE"))

fileConfig(config.config_file_name)

target_metadata = Base.metadata

ctx_var: ContextVar[dict[str, Any]] = ContextVar("ctx_var")


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    try:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()
    except AttributeError:
        context_data = ctx_var.get()
        with EnvironmentContext(
                config=context_data["config"],
                script=context_data["script"],
                **context_data["opts"],
        ):
            context.configure(connection=connection, target_metadata=target_metadata)
            with context.begin_transaction():
                context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    try:
        current_loop = asyncio.get_running_loop()
    except RuntimeError:
        asyncio.run(run_async_migrations())
        return
    from tests.test_routes import conftest
    ctx_var.set({
        "config": context.config,
        "script": context.script,
        "opts": context._proxy.context_opts,
    })
    conftest.MIGRATION_TASK = asyncio.create_task(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
