"""Exceções relacionadas
com o uso de ferramentas.
"""


class InvalidTable(Exception):
    """Exceção levantada quando uma tabela
    inválida tenta ser utilizada.
    """


class UnknownColumn(Exception):
    """Exceção levantada quando um coluna
    desconhecida tenta ser utilizada.
    """
