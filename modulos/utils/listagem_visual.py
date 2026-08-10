from dataclasses import dataclass
from html import escape
from typing import Any, Callable
import streamlit as st

# Classes de dados que representa uma coluna na listagem, com título, valor, proporção, tipo e subtítulo
@dataclass
class ColunaListagem:
    titulo: str
    valor: Callable[[Any], Any]
    proporcao: float = 1
    tipo: str = "texto"
    subtitulo: str | Callable[[Any], Any] | None = None

# Função para obter as iniciais de um nome
def obterIniciais(nome):
    partes = str(nome or "").strip().split()

    if not partes:
        return "?"

    if len(partes) == 1:
        return partes[0][:2].upper()

    return f"{partes[0][0]}{partes[-1][0]}".upper()

# Função para resolver o valor de uma coluna, seja ele um valor direto ou uma função
def resolverValor(valor, item):
    return valor(item) if callable(valor) else valor

# Função para normalizar o valor, retornando "Não informado" se for None ou vazio
def normalizarValor(valor):
    if valor is None:
        return "Não informado"

    valor = str(valor).strip()

    return valor if valor else "Não informado"

# Função para obter o texto de pesquisa de um item, concatenando os valores das colunas e subtítulos
def obterTextoPesquisa(item, colunas):
    valores = []

    for coluna in colunas:
        valores.append(
            normalizarValor(
                resolverValor(coluna.valor, item)
            )
        )

        if coluna.subtitulo is not None:
            valores.append(
                normalizarValor(
                    resolverValor(coluna.subtitulo, item)
                )
            )

    return " ".join(valores).casefold()

# Função para renderizar uma célula da tabela, dependendo do tipo da coluna
def renderizarCelula(coluna, item, primeiraColuna=False):
    valor = normalizarValor(
        resolverValor(coluna.valor, item)
    )

    valorSeguro = escape(valor)

    if coluna.tipo == "principal":
        subtitulo = ""

        if coluna.subtitulo is not None:
            subtitulo = normalizarValor(
                resolverValor(coluna.subtitulo, item)
            )

        st.html(
            f"""
            <span class="lv-row-marker"></span>

            <div class="lv-person">
                <div class="lv-avatar">
                    {escape(obterIniciais(valor))}
                </div>

                <div class="lv-person-information">
                    <div class="lv-person-name">
                        {valorSeguro}
                    </div>

                    <div class="lv-person-subtitle">
                        {escape(subtitulo)}
                    </div>
                </div>
            </div>
            """
        )

        return

    marcador = (
        '<span class="lv-row-marker"></span>'
        if primeiraColuna
        else ""
    )

    if coluna.tipo == "badge":
        st.html(
            f"""
            {marcador}

            <div class="lv-highlight">
                <span class="lv-highlight-dot"></span>

                <span>
                    {valorSeguro}
                </span>
            </div>
            """
        )

        return

    st.html(
        f"""
        {marcador}

        <div class="lv-cell-wrapper">
            <div class="lv-cell">
                {valorSeguro}
            </div>
        </div>
        """
    )

# Função principal para renderizar a listagem de itens, com cabeçalho, pesquisa e ações
def renderizarListagem(
    *,
    itens,
    categoria,
    titulo,
    descricao,
    singular,
    plural,
    colunas,
    obter_id,
    ao_visualizar,
    ao_voltar,
    prefixo_chave,
    mensagem_vazia=None,
    titulo_tabela="Registros cadastrados",
):
    aplicarEstiloListagem()

    st.html('<span class="lv-page-marker"></span>')

    itens = list(itens or [])

    colVoltar, _ = st.columns([1.05, 5.95])

    with colVoltar:
        st.html('<span class="lv-nav-marker"></span>')

        if st.button(
            "Voltar",
            icon=":material/arrow_back:",
            key=f"{prefixo_chave}_voltar",
            width="stretch",
        ):
            ao_voltar()

    st.html(
        f"""
        <div class="lv-header">
            <div class="lv-eyebrow">
                {escape(categoria)}
            </div>

            <h1 class="lv-title">
                {escape(titulo)}
            </h1>

            <p class="lv-description">
                {escape(descricao)}
            </p>
        </div>
        """
    )

    with st.container(border=True):

        st.html('<span class="lv-table-marker"></span>')

        colunaInformacao, colunaPesquisa = st.columns(
            [3.8, 2.2],
            vertical_alignment="center",
        )

        with colunaPesquisa:
            pesquisa = st.text_input(
                "Buscar",
                placeholder="Buscar...",
                icon=":material/search:",
                label_visibility="collapsed",
                key=f"{prefixo_chave}_pesquisa",
                disabled=not itens,
            )

        pesquisaNormalizada = pesquisa.strip().casefold()

        if pesquisaNormalizada:
            itensFiltrados = [
                item
                for item in itens
                if pesquisaNormalizada
                in obterTextoPesquisa(item, colunas)
            ]
        else:
            itensFiltrados = itens

        quantidadeTotal = len(itens)
        quantidadeExibida = len(itensFiltrados)

        if pesquisaNormalizada:
            textoQuantidade = (
                f"{quantidadeExibida} de "
                f"{quantidadeTotal} resultados"
            )
        elif quantidadeTotal == 1:
            textoQuantidade = f"1 {singular}"
        else:
            textoQuantidade = (
                f"{quantidadeTotal} {plural}"
            )

        with colunaInformacao:
            st.html(
                f"""
                <div class="lv-table-information">
                    <div class="lv-table-title">
                        {escape(titulo_tabela)}
                    </div>

                    <div class="lv-table-count">
                        <span class="lv-count-dot"></span>
                        {escape(textoQuantidade)}
                    </div>
                </div>
                """
            )

        st.html('<div class="lv-divider"></div>')

        if not itensFiltrados:
            mensagem = (
                "Nenhum resultado encontrado para a busca."
                if pesquisaNormalizada
                else (
                    mensagem_vazia
                    or f"Nenhum {singular} foi encontrado."
                )
            )

            st.html(
                f"""
                <div class="lv-empty">
                    {escape(mensagem)}
                </div>
                """
            )

            return

        proporcoes = [
            coluna.proporcao
            for coluna in colunas
        ]

        proporcoes.append(0.85)

        colunasCabecalho = st.columns(
            proporcoes,
            vertical_alignment="center",
        )

        for colunaStreamlit, coluna in zip(
            colunasCabecalho[:-1],
            colunas,
        ):
            with colunaStreamlit:
                st.html(
                    f"""
                    <div class="lv-column-label">
                        {escape(coluna.titulo)}
                    </div>
                    """
                )

        with colunasCabecalho[-1]:
            st.html(
                """
                <div class="lv-column-label lv-action-label">
                    Ação
                </div>
                """
            )

        st.html('<div class="lv-divider"></div>')

        for indice, item in enumerate(itensFiltrados):

            colunasLinha = st.columns(
                proporcoes,
                vertical_alignment="center",
            )

            for posicao, (colunaStreamlit, coluna) in enumerate(
                zip(colunasLinha[:-1], colunas)
            ):
                with colunaStreamlit:
                    renderizarCelula(
                        coluna,
                        item,
                        primeiraColuna=posicao == 0,
                    )

            with colunasLinha[-1]:
                visualizar = st.button(
                    "Ver",
                    icon=":material/visibility:",
                    key=(
                        f"{prefixo_chave}_visualizar_"
                        f"{obter_id(item)}"
                    ),
                    help=f"Visualizar {singular}",
                    width="stretch",
                )

            if visualizar:
                ao_visualizar(item)

            if indice < len(itensFiltrados) - 1:
                st.html('<div class="lv-divider"></div>')

# Função para aplicar o estilo CSS personalizado à listagem
def aplicarEstiloListagem():
    st.html(
        """
        <style>
        [data-testid="stMainBlockContainer"]:has(.lv-page-marker) {
            width: 100%;
            max-width: 1280px !important;

            margin-right: auto !important;
            margin-left: auto !important;

            padding-top: 4.25rem !important;
            padding-right: 2.5rem;
            padding-bottom: 4rem;
            padding-left: 2.5rem;
        }

        .lv-page-marker,
        .lv-table-marker,
        .lv-row-marker,
        .lv-nav-marker {
            display: none;
        }

        [data-testid="stElementContainer"]:has(.lv-page-marker),
        [data-testid="stElementContainer"]:has(.lv-nav-marker),
        [data-testid="stElementContainer"]:has(.lv-table-marker) {
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        [data-testid="stHorizontalBlock"]:has(.lv-nav-marker) {
            margin-bottom: 0.7rem;
        }

        .lv-header {
            position: relative;

            margin: 0.6rem 0 1.25rem;
            padding: 0 0 1.2rem 1.05rem;

            border-bottom:
                1px solid rgba(148, 163, 184, 0.13);
        }

        .lv-header::before {
            content: "";

            position: absolute;
            top: 0.18rem;
            bottom: 1.2rem;
            left: 0;

            width: 3px;

            background: #C49A4A;
            border-radius: 999px;
        }

        .lv-eyebrow {
            margin-bottom: 0.3rem;

            color: #8190A4;

            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .lv-title {
            margin: 0;

            color: #F4F7FB;

            font-size: 2rem;
            font-weight: 780;
            letter-spacing: -0.035em;
            line-height: 1.15;
        }

        .lv-description {
            max-width: 760px;

            margin: 0.42rem 0 0;

            color: #8D9AAC;

            font-size: 0.87rem;
            line-height: 1.45;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.lv-table-marker) {
            overflow: hidden;

            width: 100%;

            background:
                linear-gradient(
                    180deg,
                    rgba(10, 23, 40, 0.98),
                    rgba(7, 18, 32, 0.98)
                );

            border:
                1px solid rgba(148, 163, 184, 0.16) !important;

            border-radius: 14px !important;

            box-shadow:
                0 16px 45px rgba(0, 0, 0, 0.16);
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.lv-table-marker)
        [data-testid="stVerticalBlock"] {
            gap: 0.2rem;
        }

        .lv-table-information {
            padding: 0.25rem 0;
        }

        .lv-table-title {
            color: #DDE5EF;

            font-size: 0.88rem;
            font-weight: 700;
        }

        .lv-table-count {
            display: flex;
            align-items: center;
            gap: 0.43rem;

            margin-top: 0.18rem;

            color: #77869A;

            font-size: 0.72rem;
        }

        .lv-count-dot {
            width: 5px;
            height: 5px;

            background: #C49A4A;
            border-radius: 50%;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.lv-table-marker)
        [data-testid="stTextInput"] {
            margin: 0;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.lv-table-marker)
        [data-baseweb="input"] > div {
            min-height: 38px;

            background: rgba(5, 13, 24, 0.82) !important;

            border:
                1px solid rgba(148, 163, 184, 0.18) !important;

            border-radius: 9px !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.lv-table-marker)
        [data-baseweb="input"]:focus-within > div {
            border-color:
                rgba(196, 154, 74, 0.48) !important;

            box-shadow:
                0 0 0 2px rgba(196, 154, 74, 0.08) !important;
        }

        .lv-divider {
            width: 100%;
            height: 1px;

            margin: 0.45rem 0;

            background: rgba(148, 163, 184, 0.11);
        }

        .lv-column-label {
            width: 100%;

            color: #718096;

            font-size: 0.63rem;
            font-weight: 800;
            letter-spacing: 0.085em;
            line-height: 1.3;
            text-align: left;
            text-transform: uppercase;
        }

        .lv-action-label {
            text-align: center;
        }

        [data-testid="stHorizontalBlock"]:has(.lv-row-marker) {
            position: relative;

            min-height: 62px;

            align-items: center;

            padding: 0.48rem 0.45rem;

            border-radius: 9px;

            transition:
                background 150ms ease,
                box-shadow 150ms ease;
        }

        [data-testid="stHorizontalBlock"]:has(.lv-row-marker)::before {
            content: "";

            position: absolute;
            top: 13px;
            bottom: 13px;
            left: 0;

            width: 2px;

            background: transparent;
            border-radius: 999px;

            transition: background 150ms ease;
        }

        [data-testid="stHorizontalBlock"]:has(.lv-row-marker):hover {
            background: rgba(20, 39, 64, 0.58);

            box-shadow:
                inset 0 0 0 1px rgba(148, 163, 184, 0.05);
        }

        [data-testid="stHorizontalBlock"]:has(.lv-row-marker):hover::before {
            background: #C49A4A;
        }

        .lv-cell-wrapper {
            display: flex;
            align-items: center;
            justify-content: flex-start;

            width: 100%;
            min-height: 40px;
        }

        .lv-cell {
            width: 100%;

            color: #BAC5D3;

            font-size: 0.8rem;
            line-height: 1.45;
            text-align: left;

            overflow-wrap: anywhere;
            white-space: normal;
        }

        .lv-person {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 0.75rem;

            width: 100%;
        }

        .lv-avatar {
            width: 36px;
            height: 36px;
            flex: 0 0 36px;

            display: flex;
            align-items: center;
            justify-content: center;

            color: #D9B96F;
            background: rgba(196, 154, 74, 0.08);

            border:
                1px solid rgba(196, 154, 74, 0.25);

            border-radius: 9px;

            font-size: 0.68rem;
            font-weight: 850;
        }

        .lv-person-information {
            min-width: 0;
        }

        .lv-person-name {
            color: #E8EDF4;

            font-size: 0.86rem;
            font-weight: 690;
            line-height: 1.35;

            overflow-wrap: anywhere;
            white-space: normal;
        }

        .lv-person-subtitle {
            margin-top: 0.12rem;

            color: #718095;

            font-size: 0.67rem;
            line-height: 1.3;
        }

        .lv-highlight {
            display: flex;
            align-items: flex-start;
            justify-content: flex-start;
            gap: 0.45rem;

            width: 100%;

            color: #BCC7D4;

            font-size: 0.77rem;
            font-weight: 620;
            line-height: 1.4;
            text-align: left;

            overflow-wrap: anywhere;
            white-space: normal;
        }

        .lv-highlight-dot {
            width: 5px;
            height: 5px;
            flex: 0 0 5px;

            margin-top: 0.43rem;

            background: #C49A4A;
            border-radius: 50%;
        }

        [data-testid="stHorizontalBlock"]:has(.lv-row-marker)
        [data-testid="stBaseButton-secondary"] {
            min-height: 34px;

            padding: 0.25rem 0.55rem;

            color: #AAB7C7 !important;
            background: transparent !important;

            border:
                1px solid rgba(148, 163, 184, 0.19) !important;

            border-radius: 8px !important;

            font-size: 0.72rem !important;
            font-weight: 650 !important;
        }

        [data-testid="stHorizontalBlock"]:has(.lv-row-marker)
        [data-testid="stBaseButton-secondary"]:hover {
            color: #D9BA73 !important;

            background:
                rgba(196, 154, 74, 0.07) !important;

            border-color:
                rgba(196, 154, 74, 0.38) !important;
        }

        .lv-empty {
            padding: 2.7rem 1.5rem;

            color: #8391A3;

            font-size: 0.84rem;
            text-align: center;
        }

        @media (max-width: 900px) {
            [data-testid="stMainBlockContainer"]:has(.lv-page-marker) {
                padding-right: 1rem;
                padding-left: 1rem;
            }

            .lv-title {
                font-size: 1.65rem;
            }
        }
        </style>
        """
    )