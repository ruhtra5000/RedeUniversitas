import re
import streamlit as st

# FUNÇÕES GERAIS

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


# Função para formatar o CNPJ
def formatar_cnpj(cnpj):
    numeros = re.sub(r"\D", "", cnpj or "")

    if len(numeros) != 14:
        return cnpj or "Não informado"

    return (
        f"{numeros[:2]}.{numeros[2:5]}."
        f"{numeros[5:8]}/{numeros[8:12]}-"
        f"{numeros[12:]}"
    )


# Função para formatar uma data
def formatar_data(data):
    if data is None:
        return "Não informada"

    return data.strftime("%d/%m/%Y")


# Função para formatar um valor monetário
def formatar_moeda(valor):
    if valor is None:
        return "Não informado"

    valor_formatado = f"{valor:,.2f}"

    valor_formatado = (
        valor_formatado
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    return f"R$ {valor_formatado}"


# BOLSA

# Função para formatar o percentual de desconto
def formatar_percentual(valor):
    if valor is None:
        return "Não informado"

    return f"{float(valor) * 100:.0f}%"


# Função para formatar o status da bolsa
def formatar_status(status):
    if status is None:
        return "Não informado"

    valor_status = (
        status.value
        if hasattr(status, "value")
        else str(status)
    )

    return (
        str(valor_status)
        .replace("_", " ")
        .title()
    )


# COMPRA

# Função para obter o nome do produto da compra
def obter_nome_produto(compra):
    if compra.produto is None:
        return f"Produto #{compra.produto_id}"

    return (
        getattr(compra.produto, "nome", None)
        or f"Produto #{compra.produto_id}"
    )


# CURSO

# Função para formatar a modalidade do curso
def formatar_modalidade(modalidade):
    if modalidade is None:
        return "Não informada"

    nome_modalidade = (
        modalidade.name
        if hasattr(modalidade, "name")
        else str(modalidade)
    )

    return (
        nome_modalidade
        .replace("_", " ")
        .title()
    )

# Função para formatar a mensalidade
def formatar_mensalidade(valor):
    if valor is None:
        return "Não informada"

    valor_formatado = f"{float(valor):,.2f}"

    valor_formatado = (
        valor_formatado
        .replace(",", "#")
        .replace(".", ",")
        .replace("#", ".")
    )

    return f"R$ {valor_formatado}"


# MATRÍCULA

# Função para formatar a situação da matrícula
def formatar_aprovacao(aprovacao):
    if aprovacao is True:
        return "Aprovado"

    if aprovacao is False:
        return "Reprovado"

    return "Em andamento"


# PRODUTO

# Função para formatar a situação do estoque
def formatar_estoque(produto):
    if produto.qtde <= 0:
        return "Sem estoque"

    if produto.qtde <= produto.qtde_min:
        return (
            f"{produto.qtde} — Estoque baixo"
        )

    return f"{produto.qtde} unidades"