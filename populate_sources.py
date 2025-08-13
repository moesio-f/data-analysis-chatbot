"""Script para popular
a lista de fontes de dados
disponíveis no sistema.
"""

import os

import requests

if __name__ == "__main__":
    url = os.getenv("DATA_SOURCE_API_URL", "http://localhost:8083").rstrip()
    if not requests.get(f"{url}/list").json():
        requests.post(
            f"{url}/create",
            json={
                "name": "ghcn",
                "description": "Global Historical Climatology Network – Daily (GHCN-Daily or GHCNd)",
                "columns": [
                    {"name": "ID", "description": "Identificador da estação."},
                    {"name": "DATE", "description": "Data da observação."},
                    {"name": "ELEMENT", "description": "Tipo do elemento mensurado."},
                    {
                        "name": "DATA_VALUE",
                        "description": "Valor observado (unidade varia por elemento).",
                    },
                ],
                "connection_string": "s3://noaa-ghcn-pds/csv/by_year/2025.csv",
                "connector": "s3",
            },
        )
