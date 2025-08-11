"""API para configuração de
fontes de dados.
"""

from fastapi import FastAPI

app = FastAPI()


@app.post("/create")
def create_source(): ...


@app.get("/list")
def list_sources(): ...
