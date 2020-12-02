# -*- coding: utf-8 -*-

import unittest
import logging
from ingester import DbProvider

logging.basicConfig(
    format="%(asctime)s %(levelname)s(): %(message)s", level=logging.DEBUG
)


class TestIngester(unittest.TestCase):
    """Ingester cases."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_db_provider(self):
        db_factory = DbProvider()
        db_factory.register_builder("pgsql", PgSqlDbBuilder)
