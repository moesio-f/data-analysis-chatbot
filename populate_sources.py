"""Script para popular
a lista de fontes de dados
disponíveis no sistema.
"""

import os

import requests

if __name__ == "__main__":
    url = f"{os.getenv("DATA_SOURCE_API_URL", "http://localhost:8083").rstrip()}"
    if not requests.get(f"{url}/list").json():
        url = f"{url}/create"
        requests.post(
            url,
            json={
                "name": "btc-historical-data",
                "description": (
                    "Histórico da cotação do Bitcoin (BTC) em USD ($). "
                    "As colunas de preço podem estar armazenados como texto, sendo "
                    "necessário realizar conversões nas queries."
                ),
                "columns": [
                    {
                        "name": "Date",
                        "description": (
                            "Data de referência. Representada no "
                            "formato `Mês Dia, Ano`, com o mês em inglês e abreviado."
                        ),
                    },
                    {"name": "Price", "description": "Valor de fechamento. "},
                    {"name": "Open", "description": "Valor de abertura."},
                    {"name": "High", "description": "Valor máximo do dia."},
                    {"name": "Low", "description": "Valor mínimo do dia."},
                    {"name": "Vol.", "description": "Volume de negociações."},
                    {
                        "name": "Change %",
                        "description": "Variação percentual.",
                    },
                ],
                "connection_string": (
                    "https://github.com/MainakRepositor/Datasets/"
                    "raw/refs/heads/master/Bitcoin%20Historical%20Data.csv"
                ),
                "connector": "s3",
            },
        )

        requests.post(
            url,
            json={
                "name": "neurotech-challenge",
                "description": (
                    "Dataset para um desafio do seguinte problema de negócio: "
                    "um cientista de dados deverá desenvolver um modelo de "
                    "concessão de crédito (classificação binária)."
                ),
                "columns": [
                    {
                        "name": "REF_DATE",
                        "description": "Data de referência do registro.",
                    },
                    {
                        "name": "TARGET",
                        "description": (
                            "Alvo binário de inadimplência "
                            "(0: Bom pagador, 1: Mau Pagador)."
                        ),
                    },
                    {
                        "name": "VAR2",
                        "description": "Sexo do indívido (F, M ou NULL).",
                    },
                    {"name": "IDADE", "description": "Idade do indivíduo."},
                    {
                        "name": "VAR4",
                        "description": "Flag de óbito. Indica se o indivíduo faleceu.",
                    },
                    {
                        "name": "VAR5",
                        "description": "Unidade federativa (UF) Brasileira.",
                    },
                    {"name": "VAR8", "description": "Classe social estimada."},
                ],
                "connection_string": (
                    "https://github.com/Neurolake/challenge"
                    "-data-scientist/raw/refs/heads/main/datasets/credit_01/train.gz"
                ),
                "connector": "s3",
            },
        )
