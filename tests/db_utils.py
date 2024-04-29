
from argparse import Namespace
from pathlib import Path
from typing import Optional

from alembic.config import Config as AlembicConfig


def make_alembic_config(
    cmd_opts: Namespace
) -> AlembicConfig:
    base_path = Path("")
    if not Path(cmd_opts.config).is_absolute():
        cmd_opts.config = str(base_path.joinpath(cmd_opts.config).absolute())
    config = AlembicConfig(
        file_=cmd_opts.config,
        ini_section=cmd_opts.name,
        cmd_opts=cmd_opts,
    )
    alembic_location = config.get_main_option("script_location")
    if not Path(alembic_location).is_absolute():
        config.set_main_option(
            "script_location", str(base_path.joinpath(alembic_location).absolute())
        )
    if cmd_opts.pg_url:
        config.set_main_option("sqlalchemy.url", cmd_opts.pg_url)
    return config


def alembic_config_from_url(pg_url: Optional[str] = None) -> AlembicConfig:
    cmd_options = Namespace(
        config="alembic.ini",
        name="alembic",
        pg_url=pg_url,
        raiseerr=True,
        x=None,
    )
    return make_alembic_config(cmd_opts=cmd_options)