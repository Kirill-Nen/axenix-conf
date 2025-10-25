from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .base import Base
from .config import settings
from .models import *

engine = create_engine(
    url=settings._getDSN()
)

sessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

def create_session() -> Session:
    return sessionLocal()

def init_models():
    Base.metadata.create_all(bind=engine)