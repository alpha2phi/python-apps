# -*- coding: utf-8 -*-
#
# Import excel file into any databases.

import logging
import os
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine, inspect

__all__ = ["__version__", "DbProvider", "PgSqlDbBuilder", "PgSqlDb", "ingest"]

__version__ = "0.0.1"


logging.basicConfig(
    format="%(asctime)s %(levelname)s(): %(message)s", level=logging.DEBUG
)


def auto_str(cls):
    """Auto generate string representation of the object.

    Args:
        cls: Class for which to generate the __str__ method.
    """

    def __str__(self):
        return "%s(%s)" % (
            type(self).__name__,
            ", ".join("%s=%s" % item for item in vars(self).items()),
        )

    cls.__str__ = __str__
    return cls


class ObjectFactory:
    """Generic object factory."""

    def __init__(self):
        self._builders = {}

    def register_builder(self, key, builder):
        self._builders[key] = builder

    def create(self, key, **kwargs):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)


class DbProvider(ObjectFactory):
    """Database factory."""

    def get(self, id, **kwargs):
        """Create the database interface"""
        return self.create(id, **kwargs)


class PgSqlDbBuilder:
    """PostgreSQL database builder."""

    def __init__(self):
        self._instance = None

    def __call__(self, **_ignored):
        if not self._instance:
            # Load settings from .env
            load_dotenv(find_dotenv())
            self._instance = PgSqlDb(
                os.getenv("POSTGRES_HOST"),
                os.getenv("POSTGRES_PORT"),
                os.getenv("POSTGRES_DB"),
                os.getenv("POSTGRES_USER"),
                os.getenv("POSTGRES_PASSWORD"),
            )

        return self._instance


@auto_str
class PgSqlDb:
    """PostgreSQL database service."""

    def __init__(self, host, port, db, user, password):
        self._host = host
        self._port = port
        self._db = db
        self._user = user
        self._password = password

    def get_engine(self):
        """Create and return sqlalchemy engine."""
        return create_engine(self.get_conn_str())

    def get_conn_str(self):
        """Return the connection string."""
        return f"postgresql+psycopg2://{self._user}:{self._password}@{self._host}:{self._port}/{self._db}"


# Register database providers
db_provider = DbProvider()
db_provider.register_builder("pgsql", PgSqlDbBuilder())


def ingest(excel_file, db_name, table_name, db_type="pgsql", schema=None):
    """Ingest the file into the database table."""
    logging.info(
        f"file = {excel_file}, db = {db_name}, table = {table_name}, db type = {db_type}"
    )

    # Create database engine
    db = db_provider.get(db_type)
    engine = db.get_engine()

    # Inspect the target table schema
    inspector = inspect(engine)
    dtypes = {}
    for column in inspector.get_columns(table_name, schema=schema):
        dtypes[column["name"]] = column["type"]
    logging.info(dtypes)

    # Load the excel into database
    df = pd.read_excel(excel_file, engine="openpyxl")
    df.to_sql(
        table_name, engine, if_exists="append", chunksize=500, index=False, dtype=dtypes
    )

    # TODO - Validation
    print(f"\nTotal records in {excel_file} - {len(df)}")
    for c in df.columns:
        print(f"{c} - {df[c].nunique()}")
