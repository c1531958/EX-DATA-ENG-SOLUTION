import os

import pytest
from utils import postgres_utils


def ensure_automated_test_vars_set():
    """A function used to break integration test if the environment variable not set. Useful to
    avoid modifying resources in tables in the main databse
    """
    try:
        assert os.environ.get("IS_AUTOMATED_TEST", "").lower() == "true"
        os.environ["DB_NAME"] = "testdb"
        os.environ["HOST"] = "127.0.0.1"
        os.environ["PORT"] = "5432"
    except AssertionError:
        raise RuntimeError("Automated test variable not set")


@pytest.fixture(scope="session")
def create_test_db():
    ensure_automated_test_vars_set()
    test_db_name = os.environ["DB_NAME"]
    pg = postgres_utils.PostgresUtils()
    pg.connect_server()
    pg.get_cursor()
    pg.cursor.execute(f"CREATE DATABASE {test_db_name}")
    yield
    pg.cursor.execute(f"DROP DATABASE {test_db_name}")
    pg.connection.close()


@pytest.fixture(scope="session")
def test_db():
    ensure_automated_test_vars_set()
    pg = postgres_utils.PostgresUtils()
    pg.connect()
    pg.get_cursor()
    yield pg
    pg.connection.close()
