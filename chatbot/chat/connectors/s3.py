"""Conector para conjunto
de dados armazenados em buckets
S3-compatible.
"""

import duckdb
import pandas as pd
from chat.entities import Connector


class DuckDBS3Connector(Connector):
    """Conector para fontes
    de dados no S3.

    Essa classe implementa um
    conector baseado no `duckdb`
    para realizar queries em arquivos
    tabulares armazenados remotamente.

    A implementação atual carrega o
    banco localmente (in-memory) para
    maior performance nas queries.
    """

    def __init__(self, connection_string: str, table: str):
        assert any(
            connection_string.startswith(p) for p in ("gs://", "s3://", "https://")
        ), "Unsupported schema (must be gs://, s3:// or https://)."

        # Special case of `.gz` files without extension;
        #   Required to load some non-standard datasets names
        if connection_string.endswith(".gz") and not connection_string.endswith(
            ".csv.gz"
        ):
            self._include_read_csv = True
        else:
            assert any(
                connection_string.endswith(p) for p in (".parquet", ".csv", ".csv.gz")
            ), "Only CSV/Parquet are supported."
            self._include_read_csv = False

        super().__init__(connection_string, table)
        self._connection = None

    def connect(self):
        if self._connection is not None:
            return

        self._connection = duckdb.connect(":memory:")
        self._connection.sql("INSTALL httpfs; LOAD httpfs;")
        ds_read = "read_csv('{}')" if self._include_read_csv else "'{}'"
        self._connection.sql(
            f"CREATE TABLE '{self.table}' AS SELECT "
            f"* FROM {ds_read.format(self.connection_string)};"
        )

    def disconnect(self):
        if self._connection is None:
            return

        self._connection.close()
        self._connection = None

    def query(self, query: str) -> pd.DataFrame:
        self._connection.execute(query)
        return self._connection.fetch_df()
