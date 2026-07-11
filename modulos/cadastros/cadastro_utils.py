import re

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$")

def validarEmail(email: str) -> bool:
    return EMAIL_REGEX.fullmatch(email) is not None


def validarTelefone(telefone: str) -> bool:
    return re.fullmatch(r"\d{11}", telefone) is not None