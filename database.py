from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALACHEMY_DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(
    SQLALACHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    with sessionlocal() as db:
        yield db

