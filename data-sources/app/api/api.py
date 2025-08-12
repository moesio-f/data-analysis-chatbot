"""API para configuração de
fontes de dados.
"""

import logging
from contextlib import asynccontextmanager

import app.database as db
from app.config import settings
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.orm.exc import NoResultFound

from . import models
from .db import RequiresSession, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lógica de start-up e shutdown.

    Realiza a criação das tabelas no
    banco de dados.
    """
    LOGGER.debug("Creating tables...")
    try:
        db.Base.metadata.create_all(engine)
    except Exception as e:
        LOGGER.critical("Unable to create table: %s", e, exc_info=True)
        exit(-1)
    LOGGER.debug("Tables created.")
    yield


LOGGER = logging.getLogger(__name__)
app = FastAPI(lifespan=lifespan, debug=settings.run_with_debug)


@app.post("/create")
def create_source(
    ds: models.DataSourceInput, session: Session = RequiresSession
) -> models.DataSource:
    """Cria uma nova fonte de dados
    no sistema.
    """
    try:
        ds = db.DataSource(
            name=ds.name,
            description=ds.description,
            connection_string=ds.connection_string,
            connector=ds.connector,
            columns=[
                db.ColumnDescription(name=col.name, description=col.description)
                for col in ds.columns
            ],
        )
        session.add(ds)
        session.commit()
    except Exception as e:
        LOGGER.error("Failed to commit transaction: %s", e, exc_info=True)
        raise
    return ds


@app.get("/list")
def list_sources(session: Session = RequiresSession) -> list[models.DataSource]:
    """Retorna todas as fontes de dados cadastradas
    no sistema.
    """
    try:
        return list(
            session.query(db.DataSource)
            .options(selectinload(db.DataSource.columns))
            .all()
        )
    except Exception as e:
        LOGGER.error("Query failed with error: %s", e, exc_info=True)
        raise


@app.get("/info/{id}")
def get_source(id: int, session: Session = RequiresSession) -> models.DataSource:
    """Retorna informações para a fonte de dados
    com esse id.
    """
    try:
        return session.query(db.DataSource).where(db.DataSource.id == id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Data source not found.")
