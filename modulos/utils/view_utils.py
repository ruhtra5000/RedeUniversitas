import re
import streamlit as st

# Função para exibir um campo com título e valor
def exibirCampo(titulo, valor):
    if valor is None or valor == "":
        valor = "Não informado"

    with st.container(border=True):
        st.caption(titulo)
        st.markdown(f"**{valor}**")

# Função para formatar o percentual de desconto da bolsa
def formatarPercentual(valor):
    if valor is None:
        return "Não informado"

    return f"{float(valor) * 100:.0f}%"

# Função para formatar a data de início da bolsa
def formatarData(data):
    if data is None:
        return "Não informada"

    return data.strftime("%d/%m/%Y")

# Função para formatar o status da bolsa
def formatarStatus(status):
    if status is None:
        return "Não informado"

    valor = status.value if hasattr(status, "value") else str(status)

    return str(valor).replace("_", " ").title()

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

    nome = modalidade.name if hasattr(modalidade, "name") else str(modalidade)

    return nome.replace("_", " ").title()

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

# Função para formatar a aprovação
def formatarAprovacao(aprovacao):
    if aprovacao is True:
        return "Aprovado"

    if aprovacao is False:
        return "Reprovado"

    return "Em andamento"