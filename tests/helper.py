from __future__ import annotations

import os
import secrets
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


@dataclass
class DBSettings:
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    @staticmethod
    def from_env() -> DBSettings:
        test_dir = os.path.dirname(__file__)
        dotenv_path = os.path.join(os.path.dirname(test_dir), ".env")
        load_dotenv(dotenv_path=dotenv_path)
        return DBSettings(
            db_user=os.environ["POSTGRES_USER"],
            db_password=os.environ["POSTGRES_PASSWORD"],
            db_host=os.environ["POSTGRES_HOST"],
            db_port=os.environ["POSTGRES_PORT"],
            db_name=os.environ.get("DATABASE_NAME", "postgres"),
        )

    def set_database_name(self, db_name: str) -> DBSettings:
        self.db_name = db_name
        return self

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


class DatabaseManager:
    def __init__(self, settings: DBSettings) -> None:
        self._settings = settings
        self._maintenance_engine = create_engine(self._settings.database_url)

    @contextmanager
    def engine(self, db_url: str) -> Generator[Engine, None, None]:
        engine = create_engine(db_url)
        try:
            yield engine
        finally:
            engine.dispose()

    @contextmanager
    def database(self, db_name: str) -> Generator[str, None, None]:
        unique_db_name = f"{db_name}_{secrets.token_hex(8)}"
        self._create(unique_db_name)
        try:
            yield self._settings.set_database_name(unique_db_name).database_url
        finally:
            self._drop(unique_db_name)

    def _create(self, db_name: str) -> None:
        with self._maintenance_engine.begin() as connection:
            connection.execute(text("COMMIT"))
            connection.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
            connection.execute(text(f"CREATE DATABASE {db_name}"))

    def _drop(self, db_name: str) -> None:
        with self._maintenance_engine.begin() as connection:
            connection.execute(text("COMMIT"))
            connection.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
