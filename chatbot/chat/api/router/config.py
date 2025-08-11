"""Endpoints de configuração de
fontes de dados.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/data-source", tags=["Data Source"])


@router.post("/create")
def create_source(): ...


@router.get("/list")
def list_sources(): ...
