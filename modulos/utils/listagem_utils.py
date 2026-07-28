import re
import streamlit as st

# Função para criar um separador horizontal estilizado
def separador():
    st.markdown(
        '<hr style="'
        'margin: 0.45rem 0;'
        'border: none;'
        'border-top: 1px solid rgba(128, 128, 128, 0.25);'
        '">',
        unsafe_allow_html=True,
    )

# Função para formatar o CPF
def formatar_cpf(cpf):
    numeros = re.sub(r"\D", "", cpf or "")

    if len(numeros) != 11:
        return cpf or "Não informado"

    return (
        f"{numeros[:3]}.{numeros[3:6]}."
        f"{numeros[6:9]}-{numeros[9:]}"
    )

# Função para formatar a modalidade
def formatar_modalidade(modalidade):
    if modalidade is None:
        return "Não informada"

    nome = (
        modalidade.name
        if hasattr(modalidade, "name")
        else str(modalidade)
    )

    return nome.replace("_", " ").title()