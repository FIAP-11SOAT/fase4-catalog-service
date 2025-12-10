import os
from app.db import _build_database_url_from_env


def test_db_url_builder_defaults():
    for k in ["DB_USER","POSTGRES_USER","DB_PASS","POSTGRES_PASSWORD","DB_HOST","DB","DB_PORT","POSTGRES_PORT","DB_NAME","POSTGRES_DB","DATABASE_URL"]:
        os.environ.pop(k, None)
    url = _build_database_url_from_env()
    assert url == "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"


def test_db_url_builder_envs():
    os.environ["DB_USER"] = "u"
    os.environ["DB_PASS"] = "p"
    os.environ["DB_HOST"] = "h"
    os.environ["DB_PORT"] = "1234"
    os.environ["DB_NAME"] = "d"
    url = _build_database_url_from_env()
    assert url == "postgresql+psycopg2://u:p@h:1234/d"
