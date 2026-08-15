import re
import streamlit as st

# FUNÇÕES GERAIS

# Função auxiliar para remover chaves do session_state
def _limpar_chaves(*chaves):
    for chave in chaves:
        st.session_state.pop(chave, None)

# Função para exibir um campo com título e valor
def exibirCampo(titulo, valor, altura=None):
    if valor is None or valor == "":
        valor = "Não informado"

    opcoes_container = {
        "border": True,
    }

    if altura is not None:
        opcoes_container["height"] = altura

    with st.container(**opcoes_container):
        st.caption(titulo)
        st.markdown(f"**{valor}**")

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


# ALUNO

# Função para limpar a consulta de aluno
def limpar_consulta_aluno():
    _limpar_chaves(
        "consulta_aluno_id",
        "consulta_cpf",
        "consulta_id",
    )

def formatar_status_aluno(aluno):
    if aluno.status is None:
        return "Não informado"

    return aluno.status.value.replace("_", " ").title()


# ALMOXARIFE

# Função para limpar a consulta de almoxarife
def limpar_consulta_almoxarife():
    _limpar_chaves(
        "consulta_almoxarife_id",
        "consulta_almoxarife_cpf",
        "consulta_almoxarife_id_digitado",
    )


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


# Função para limpar a consulta de bolsa
def limpar_consulta_bolsa():
    _limpar_chaves(
        "consulta_bolsa_id",
        "consulta_bolsa_id_digitado",
    )


# CAMPUS

# Função para limpar a consulta de campus
def limpar_consulta_campus():
    _limpar_chaves(
        "consulta_campus_id",
        "consulta_campus_cnpj",
        "consulta_campus_id_digitado",
    )


# COMPRA

# Função para limpar a consulta de compra
def limpar_consulta_compra():
    _limpar_chaves(
        "consulta_compra_id",
        "consulta_compra_id_digitado",
    )


# Função para obter o nome do produto da compra
def obter_nome_produto(compra):
    if compra.produto is None:
        return f"Produto #{compra.produto_id}"

    return (
        getattr(compra.produto, "nome", None)
        or f"Produto #{compra.produto_id}"
    )


# Função para obter o nome do responsável financeiro
def obter_nome_financeiro(compra):
    if compra.financeiro is None:
        return "Não informado"

    pessoa = getattr(
        compra.financeiro,
        "pessoa",
        None,
    )

    if pessoa:
        return pessoa.nome

    return f"Financeiro #{compra.financeiro_id}"


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


# Função para limpar a consulta de curso
def limpar_consulta_curso():
    _limpar_chaves(
        "consulta_curso_id",
        "consulta_curso_busca",
    )


# DISCIPLINA

# Função para limpar a consulta de disciplina
def limpar_consulta_disciplina():
    _limpar_chaves(
        "consulta_disciplina_id",
        "consulta_disciplina_codigo",
        "consulta_disciplina_id_digitado",
    )


# FINANCEIRO

# Função para limpar a consulta de financeiro
def limpar_consulta_financeiro():
    _limpar_chaves(
        "consulta_financeiro_id",
        "consulta_financeiro_cpf",
        "consulta_financeiro_id_digitado",
    )


# FORNECEDOR

# Função para limpar a consulta de fornecedor
def limpar_consulta_fornecedor():
    _limpar_chaves(
        "consulta_fornecedor_id",
        "consulta_fornecedor_id_digitado",
    )


# MATRÍCULA

# Função para formatar a aprovação da matrícula
def formatar_aprovacao(aprovacao):
    if aprovacao is True:
        return "Aprovado"

    if aprovacao is False:
        return "Reprovado"

    return "Em andamento"


# Função para limpar a consulta de matrícula
def limpar_consulta_matricula():
    _limpar_chaves(
        "consulta_matricula_chave",
        "consulta_matricula_aluno",
        "consulta_matricula_turma",
    )


# PRODUTO

# Função para formatar a situação do estoque
def formatar_situacao_estoque(produto):
    if produto.qtde <= 0:
        return "Sem estoque"

    if produto.qtde <= produto.qtde_min:
        return "Estoque baixo"

    return "Estoque adequado"


# Função para limpar a consulta de produto
def limpar_consulta_produto():
    _limpar_chaves(
        "consulta_produto_id",
        "consulta_produto_id_digitado",
    )


# PROFESSOR

# Função para limpar a consulta de professor
def limpar_consulta_professor():
    _limpar_chaves(
        "consulta_professor_id",
        "consulta_professor_cpf",
        "consulta_professor_id_digitado",
    )


# TURMA

# Função para limpar a consulta de turma
def limpar_consulta_turma():
    _limpar_chaves(
        "consulta_turma_id",
        "consulta_turma_codigo",
        "consulta_turma_id_digitado",
    )