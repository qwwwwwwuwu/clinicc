from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

db_user = "appuser"
db_pass = "secret"  # Здесь ваш реальный пароль
db_host = "db"
db_port = "5432"
db_name = "clinic"


encoded_pass = quote_plus(db_pass)


DATABASE_URL = f"postgresql://{db_user}:{encoded_pass}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URL)

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

print(f"Final connection string: {DATABASE_URL}")