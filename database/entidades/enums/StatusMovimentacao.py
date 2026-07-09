from enum import Enum

class StatusMovimentacao(Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"
    AJUSTE = "AJUSTE"
    PERDA = "PERDA"