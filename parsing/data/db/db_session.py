from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

SQLAlchemyBase = declarative_base()
__factory = None


def global_init(url: str):
    global __factory

    if __factory:
        return
    url = url.strip()
    if not url:
        return
    if 'postgres' in url:
        url = url.replace('postgres', 'postgresql')
    engine = create_engine(url, echo=False, poolclass=NullPool)
    __factory = sessionmaker(bind=engine)
    from . import __all_models
    SQLAlchemyBase.metadata.create_all()


def create_session() -> Session:
    global __factory
    return __factory()