import os
import os
import sys

# Ensure project root is on sys.path BEFORE importing app.*
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from app.db import Base, get_db
from app.main import app


@pytest.fixture(scope="session")
def test_engine():
    # Single in-memory SQLite shared across threads for TestClient
    os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
    engine = create_engine(
        os.environ["DATABASE_URL"],
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture()
def db_session(test_engine):
    # Ensure a clean schema per test to avoid uniqueness conflicts
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    # Hard truncate tables to ensure no residual state
    with test_engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys=OFF"))
        conn.execute(text("DELETE FROM products"))
        conn.execute(text("DELETE FROM product_categories"))
        conn.execute(text("PRAGMA foreign_keys=ON"))
        conn.commit()

    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = testing_session_local()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def override_db_dependency(db_session):
    def _get_db_override():
        yield db_session

    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides.clear()
