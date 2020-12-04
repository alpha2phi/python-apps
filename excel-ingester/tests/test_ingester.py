# -*- coding: utf-8 -*-

import unittest
import logging

import loader

logging.basicConfig(
    format="%(asctime)s %(levelname)s(): %(message)s", level=logging.DEBUG
)


class TestIngester(unittest.TestCase):
    """Ingester cases."""

    def test_db_provider(self):
        pass
        # db_factory = DbFactory()
        # db_factory.register_builder("pgsql", PgSqlDbBuilder)


if __name__ == "__main__":
    unittest.main()
