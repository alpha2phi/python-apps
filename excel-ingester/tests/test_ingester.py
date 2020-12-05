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
        db_factory = DbFactory()
        db_factory.register_builder("pgsql", PgSqlDbBuilder)
        print("okay")


if __name__ == "__main__":
    unittest.main()
