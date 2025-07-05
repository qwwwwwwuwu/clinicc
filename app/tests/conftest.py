import io
import sys
from typing import Any, Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base


class SafeStderr(io.StringIO):
    def __init__(self) -> None:
        super().__init__()
        self._real_stderr = sys.__stderr__

    def close(self) -> None:
        pass

    def write(self, msg: str) -> int:
        try:
            return super().write(msg)
        except ValueError:
            return 0

    def flush(self) -> None:
        pass

    def __getattr__(self, name: str) -> Any:
        return getattr(self._real_stderr, name)


@pytest.fixture(autouse=True)
def patch_stderr() -> Generator[None, None, None]:
    """Фикстура для временной замены sys.stderr."""
    original_stderr = sys.stderr
    sys.stderr = SafeStderr()
    yield
    sys.stderr = original_stderr


# Конфигурация тестовой БД
TEST_DATABASE_URL = "postgresql://test:test@localhost:5432/test"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def test_db() -> Generator[None, None, None]:
    """Фикстура для создания/удаления тестовых таблиц."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_db: None) -> Generator[Session, None, None]:
    """Фикстура для работы с тестовой сессией БД."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
