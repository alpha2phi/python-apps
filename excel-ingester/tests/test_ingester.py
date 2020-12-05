# -*- coding: utf-8 -*-

import unittest
import logging

from loader import *

logging.basicConfig(
    format="%(asctime)s %(levelname)s(): %(message)s", level=logging.DEBUG
)


class TestIngester(unittest.TestCase):
    """Ingester cases."""

    def test_db_provider(self):
        db_provider = DbProvider()
        db_provider.register_builder("pgsql", PgSqlDbBuilder())

        config = {
            "host": "pgsql",
            "port": 1200,
            "user": "test_user",
            "password": "test_password",
        }

        db = db_provider.get("pgsql", **config)
        assert db is not None
        logging.info(db.get_conn_str())

    def test_ingester(self):
        ingest("account", "testdb", "accounts")


if __name__ == "__main__":
    unittest.main()
