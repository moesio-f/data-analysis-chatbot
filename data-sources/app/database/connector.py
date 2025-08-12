"""Conectores disponíveis no
sistema.
"""

from enum import StrEnum


class Connector(StrEnum):
    s3 = "s3"
    postgres = "postgres"
