"""Conexão com o banco."""

import sqlalchemy as sa
from app.config import settings
from fastapi import Depends

engine = sa.create_engine(settings.database_url)


def get_db_session():
    with sa.orm.Session(engine, expire_on_commit=False) as session:
        yield session


RequiresSession = Depends(get_db_session)
