import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database import Base

# Конфигурация для тестовой БД
TEST_DATABASE_URL = "postgresql://test:test@localhost:5432/test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_db():
    """Создание и удаление таблиц БД перед/после тестов."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_db) -> Session:
    """Создание тестовой сессии с транзакцией (откат после теста)."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
