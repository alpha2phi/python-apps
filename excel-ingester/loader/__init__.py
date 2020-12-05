# -*- coding: utf-8 -*-
#
# Import excel file into any databases.

from dotenv import load_dotenv, find_dotenv

__all__ = ["__version__", "DbProvider", "PgSqlDbBuilder"]

__version__ = "0.0.1"


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

    def __call__(self, host, port, user, password, **_ignored):
        if not self._instance:
            self._instance = PgSqlDb(host, port, user, password)
        return self._instance


@auto_str
class PgSqlDb:
    """PostgreSQL database service."""

    def __init__(self, host, port, user, password):
        self._host = host
        self._port = port
        self._user = user
        self._password = password


class MySqlDb:
    """MySQL database."""

    pass


class ImpalaDb:
    """Impala database."""


def db_config_from_env():
    """Get database configurations from environment."""
    load_dotenv(find_dotenv())
