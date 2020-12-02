# -*- coding: utf-8 -*-
#
# Import excel file into any databases.

import os
import argparse
import pandas as pd


class ObjectFactory:
    """Generic object factor."""

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

    def get(self, service_id, **kwargs):
        """Cret"""
        return self.create(service_id, **kwargs)


class PgSqlDbBuilder:
    """PostgreSQL database builder."""

  def __init__(self):
        self._instance = None

    def __call__(self, host, port, user, password, **_ignored):
        if not self._instance:
            self._instance = PgSqlDb(host, port, user, password)
        return self._instance

class PgSqlDb:
    """PostgreSQL database service."""

    def __init__(self, host, port, user, password):
        self._host = host
        self._port = port
        self._user = user
        self._password = password

    def test_method():
        print("pgsql")


class MySqlDb:
    """MySQL database."""

    pass


class ImpalaDb:
    """Impala database."""


def db_config_from_env():
    """Get database configurations from environment."""
    load_dotenv(find_dotenv())
