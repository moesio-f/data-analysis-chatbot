"""Client para consumo
da API de fontes de dados.
"""

from functools import lru_cache

import requests
from chat.config import data_source_api_settings as settings
from chat.connectors.s3 import DuckDBS3Connector
from chat.entities import Column, DataSource


@lru_cache()
def get_source(data_source_id: int) -> DataSource:
    """Obtém um conjunto de dados utilizando
    a API de fontes de dados e instancia
    um conector.

    Args:
        data_source_id: ID da fonte de dados.

    Returns:
        DataSource: fonte de dados.
    """
    response: requests.Response = requests.get(
        f"{settings.url.rstrip("/")}/info/{data_source_id}"
    )
    response.raise_for_status()
    data = response.json()

    if data["connector"].lower() != "s3":
        raise NotImplementedError("Current version only supports S3 connection.")

    connector = DuckDBS3Connector(data["connection_string"], data["name"])
    connector.connect()
    columns = [
        Column(name=c["name"], description=c["description"]) for c in data["columns"]
    ]
    return DataSource(
        name=data["name"],
        description=data["description"],
        columns=columns,
        connector=connector,
    )
