from dataclasses import dataclass
from html import escape
from typing import Any, Callable
import streamlit as st

# Classes de dados para representar campos de busca, campos de visualização, seções e ações na interface do usuário.
@dataclass
class CampoBusca:
    nome: str
    rotulo: str
    placeholder: str = ""
    proporcao: float = 1
    chave: str | None = None

# Classes de dados para representar campos de visualização, seções e ações na interface do usuário.
@dataclass
class CampoView:
    rotulo: str
    valor: Any | Callable[[Any], Any]
    proporcao: float = 1
    tipo: str = "texto"

# Classes de dados para representar seções e ações na interface do usuário.
@dataclass
class SecaoView:
    titulo: str
    linhas: list[list[CampoView]]
    descricao: str | None = None

# Classes de dados para representar ações na interface do usuário.
@dataclass
class AcaoView:
    rotulo: str
    ao_clicar: Callable[[Any], None]
    icone: str | None = None
    tipo: str = "secondary"
    chave: str | None = None
    visivel: bool | Callable[[Any], bool] = True

# Funções auxiliar para resolver valores.
def resolverValor(valor, registro):
    return valor(registro) if callable(valor) else valor

# Função auxiliar para normalizar valores, retornando "Não informado" para valores nulos ou vazios.
def normalizarValor(valor):
    if valor is None:
        return "Não informado"

    valor = str(valor).strip()

    return valor if valor else "Não informado"

# Função auxiliar para obter as iniciais de um nome, retornando "?" se o nome estiver vazio.
def obterIniciais(nome):
    partes = str(nome or "").strip().split()

    if not partes:
        return "?"

    if len(partes) == 1:
        return partes[0][:2].upper()

    return f"{partes[0][0]}{partes[-1][0]}".upper()

# Função para renderizar o cabeçalho da página, incluindo categoria, título, descrição e botão de voltar.
def renderizarCabecalhoView(
    *,
    categoria,
    titulo,
    descricao,
    ao_voltar,
    prefixo_chave,
):
    aplicarEstiloView()

    st.html('<span class="vv-page-marker"></span>')

    colVoltar, _ = st.columns([1.05, 5.95])

    with colVoltar:
        st.html('<span class="vv-nav-marker"></span>')

        if st.button(
            "Voltar",
            icon=":material/arrow_back:",
            key=f"{prefixo_chave}_voltar",
            width="stretch",
        ):
            ao_voltar()

    st.html(
        f"""
        <div class="vv-header">
            <div class="vv-eyebrow">
                {escape(str(categoria))}
            </div>

            <h1 class="vv-title">
                {escape(str(titulo))}
            </h1>

            <p class="vv-description">
                {escape(str(descricao))}
            </p>
        </div>
        """
    )

# Função para renderizar o formulário de busca, incluindo campos de entrada e botão de busca.
def renderizarFormularioBusca(
    *,
    campos,
    prefixo_chave,
    titulo="Localizar registro",
    descricao="Informe um dos dados abaixo para realizar a consulta.",
    texto_botao="Buscar",
):
    valores = {}

    with st.form(
        key=f"{prefixo_chave}_form_busca",
        border=False,
    ):
        st.html('<span class="vv-search-marker"></span>')

        st.html(
            f"""
            <div class="vv-search-heading">
                <div class="vv-search-title">
                    {escape(str(titulo))}
                </div>

                <div class="vv-search-description">
                    {escape(str(descricao))}
                </div>
            </div>
            """
        )

        proporcoes = [campo.proporcao for campo in campos]
        colunas = st.columns(proporcoes)

        for colunaStreamlit, campo in zip(colunas, campos):
            with colunaStreamlit:
                chave = (
                    campo.chave
                    or f"{prefixo_chave}_{campo.nome}"
                )

                valores[campo.nome] = st.text_input(
                    campo.rotulo,
                    placeholder=campo.placeholder,
                    key=chave,
                )

        _, colunaBotao = st.columns([4.7, 1.3])

        with colunaBotao:
            buscar = st.form_submit_button(
                texto_botao,
                icon=":material/search:",
                type="primary",
                width="stretch",
            )

    return buscar, valores

# Função para renderizar um campo de visualização, incluindo rótulo e valor, com diferentes estilos dependendo do tipo de campo.
def renderizarCampoView(campo, registro):
    valor = normalizarValor(
        resolverValor(campo.valor, registro)
    )

    valorSeguro = escape(valor)

    if campo.tipo == "badge":
        conteudo = f"""
        <span class="vv-field-badge">
            <span class="vv-field-badge-dot"></span>
            {valorSeguro}
        </span>
        """
    elif campo.tipo == "destaque":
        conteudo = (
            '<span class="vv-field-value-highlight">'
            f"{valorSeguro}</span>"
        )
    elif campo.tipo == "email" and valor != "Não informado":
        conteudo = (
            f'<a href="mailto:{escape(valor, quote=True)}">'
            f"{valorSeguro}</a>"
        )
    else:
        conteudo = valorSeguro

    st.html(
        f"""
        <div class="vv-field">
            <div class="vv-field-label">
                {escape(str(campo.rotulo))}
            </div>

            <div class="vv-field-value">
                {conteudo}
            </div>
        </div>
        """
    )

# Função para renderizar a visualização de um registro, incluindo informações do registro, seções e ações disponíveis.
def renderizarRegistroView(
    *,
    registro,
    nome,
    tipo_registro,
    secoes,
    prefixo_chave,
    ao_limpar=None,
    meta=None,
    status=None,
    icone=None,
    acoes=None,
):
    nomeResolvido = normalizarValor(
        resolverValor(nome, registro)
    )

    tipoResolvido = normalizarValor(
        resolverValor(tipo_registro, registro)
    )

    metaResolvida = (
        normalizarValor(resolverValor(meta, registro))
        if meta is not None
        else None
    )

    statusResolvido = (
        normalizarValor(resolverValor(status, registro))
        if status is not None
        else None
    )

    identificador = (
        normalizarValor(resolverValor(icone, registro))
        if icone is not None
        else obterIniciais(nomeResolvido)
    )

    acoesVisiveis = []

    if ao_limpar:
        acoesVisiveis.append(
            {
                "rotulo": "Limpar",
                "icone": ":material/close:",
                "tipo": "secondary",
                "chave": "limpar",
                "ao_clicar": lambda: ao_limpar(),
            }
        )

    for acao in acoes or []:
        visivel = (
            acao.visivel(registro)
            if callable(acao.visivel)
            else acao.visivel
        )

        if visivel:
            acoesVisiveis.append(
                {
                    "rotulo": acao.rotulo,
                    "icone": acao.icone,
                    "tipo": acao.tipo,
                    "chave": acao.chave or acao.rotulo.lower(),
                    "ao_clicar": (
                        lambda acaoAtual=acao:
                        acaoAtual.ao_clicar(registro)
                    ),
                }
            )

    with st.container(border=True):
        st.html('<span class="vv-record-marker"></span>')

        proporcoes = [5.2] + [
            0.9
            for _ in acoesVisiveis
        ]

        colunas = st.columns(
            proporcoes,
            vertical_alignment="center",
        )

        with colunas[0]:
            metaHtml = (
                f'<div class="vv-record-meta">'
                f'{escape(metaResolvida)}</div>'
                if metaResolvida
                else ""
            )

            statusHtml = (
                '<div class="vv-record-status">'
                '<span class="vv-status-dot"></span>'
                f'{escape(statusResolvido)}</div>'
                if statusResolvido
                else ""
            )

            st.html(
                f"""
                <div class="vv-record">
                    <div class="vv-avatar">
                        {escape(identificador)}
                    </div>

                    <div class="vv-record-information">
                        <div class="vv-record-type">
                            {escape(tipoResolvido)}
                        </div>

                        <div class="vv-record-name">
                            {escape(nomeResolvido)}
                        </div>

                        {metaHtml}
                        {statusHtml}
                    </div>
                </div>
                """
            )

        for colunaAcao, acao in zip(
            colunas[1:],
            acoesVisiveis,
        ):
            with colunaAcao:
                if st.button(
                    acao["rotulo"],
                    icon=acao.get("icone"),
                    type=acao.get("tipo", "secondary"),
                    key=(
                        f"{prefixo_chave}_"
                        f"{acao.get('chave', 'acao')}"
                    ),
                    use_container_width=True,
                ):
                    acao["ao_clicar"]()

    for indice, secao in enumerate(secoes, start=1):
        with st.container(border=True):
            st.html('<span class="vv-section-marker"></span>')

            descricaoHtml = (
                '<div class="vv-section-description">'
                f'{escape(secao.descricao)}</div>'
                if secao.descricao
                else ""
            )

            st.html(
                f"""
                <div class="vv-section-heading">
                    <div class="vv-section-number">
                        {indice:02d}
                    </div>

                    <div>
                        <div class="vv-section-title">
                            {escape(secao.titulo)}
                        </div>

                        {descricaoHtml}
                    </div>
                </div>
                """
            )

            for linha in secao.linhas:
                proporcoes = [
                    campo.proporcao
                    for campo in linha
                ]

                colunas = st.columns(proporcoes)

                for colunaStreamlit, campo in zip(
                    colunas,
                    linha,
                ):
                    with colunaStreamlit:
                        renderizarCampoView(
                            campo,
                            registro,
                        )

# Função para renderizar uma mensagem inicial, geralmente usada quando não há registros para exibir.
def renderizarMensagemInicial(mensagem):
    st.html(
        f"""
        <div class="vv-empty-state">
            {escape(str(mensagem))}
        </div>
        """
    )

# Função para aplicar estilos CSS personalizados à interface do usuário.
def aplicarEstiloView():
    st.html(
        """
        <style>
        [data-testid="stMainBlockContainer"]:has(.vv-page-marker) {
            width: 100%;
            max-width: 1160px !important;

            margin-right: auto !important;
            margin-left: auto !important;

            padding-top: 4.25rem !important;
            padding-right: 2.5rem;
            padding-bottom: 4rem;
            padding-left: 2.5rem;
        }

        .vv-page-marker,
        .vv-nav-marker,
        .vv-search-marker,
        .vv-record-marker,
        .vv-section-marker {
            display: none;
        }

        [data-testid="stElementContainer"]:has(.vv-page-marker),
        [data-testid="stElementContainer"]:has(.vv-nav-marker),
        [data-testid="stElementContainer"]:has(.vv-search-marker),
        [data-testid="stElementContainer"]:has(.vv-record-marker),
        [data-testid="stElementContainer"]:has(.vv-section-marker) {
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        [data-testid="stHorizontalBlock"]:has(.vv-nav-marker) {
            margin-bottom: 0.7rem;
        }

        .vv-header {
            position: relative;

            margin: 0.6rem 0 1.25rem;
            padding: 0 0 1.2rem 1.05rem;

            border-bottom:
                1px solid rgba(148, 163, 184, 0.13);
        }

        .vv-header::before {
            content: "";

            position: absolute;
            top: 0.18rem;
            bottom: 1.2rem;
            left: 0;

            width: 3px;

            background: #C49A4A;
            border-radius: 999px;
        }

        .vv-eyebrow {
            margin-bottom: 0.3rem;

            color: #8190A4;

            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .vv-title {
            margin: 0;

            color: #F4F7FB;

            font-size: 2rem;
            font-weight: 780;
            letter-spacing: -0.035em;
            line-height: 1.15;
        }

        .vv-description {
            max-width: 760px;

            margin: 0.42rem 0 0;

            color: #8D9AAC;

            font-size: 0.87rem;
            line-height: 1.45;
        }

        [data-testid="stForm"]:has(.vv-search-marker) {
            margin-bottom: 1.1rem;
            padding: 1.15rem 1.25rem 1.25rem;

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
                0 14px 38px rgba(0, 0, 0, 0.14);
        }

        .vv-search-heading {
            margin-bottom: 0.9rem;
        }

        .vv-search-title {
            color: #DDE5EF;

            font-size: 0.9rem;
            font-weight: 720;
        }

        .vv-search-description {
            margin-top: 0.18rem;

            color: #77869A;

            font-size: 0.72rem;
        }

        [data-testid="stForm"]:has(.vv-search-marker)
        [data-baseweb="input"] > div {
            min-height: 40px;

            background: rgba(5, 13, 24, 0.82) !important;

            border:
                1px solid rgba(148, 163, 184, 0.18) !important;

            border-radius: 9px !important;
        }

        [data-testid="stForm"]:has(.vv-search-marker)
        [data-baseweb="input"]:focus-within > div {
            border-color:
                rgba(196, 154, 74, 0.50) !important;

            box-shadow:
                0 0 0 2px rgba(196, 154, 74, 0.08) !important;
        }

        [data-testid="stForm"]:has(.vv-search-marker)
        [data-testid="stBaseButton-primary"] {
            min-height: 39px;

            color: #07172C !important;
            background: #C49A4A !important;

            border: 1px solid #C49A4A !important;
            border-radius: 9px !important;

            font-weight: 750 !important;
        }

        [data-testid="stForm"]:has(.vv-search-marker)
        [data-testid="stBaseButton-primary"]:hover {
            background: #D5AE62 !important;
            border-color: #D5AE62 !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.vv-record-marker) {
            margin: 0.2rem 0 1rem;

            background:
                linear-gradient(
                    110deg,
                    rgba(12, 28, 49, 0.98),
                    rgba(8, 20, 36, 0.98)
                );

            border:
                1px solid rgba(148, 163, 184, 0.16) !important;

            border-left:
                3px solid #C49A4A !important;

            border-radius: 14px !important;

            box-shadow:
                0 15px 40px rgba(0, 0, 0, 0.15);
        }

        .vv-record {
            display: flex;
            align-items: center;
            gap: 0.9rem;

            min-height: 58px;
        }

        .vv-avatar {
            width: 46px;
            height: 46px;
            flex: 0 0 46px;

            display: flex;
            align-items: center;
            justify-content: center;

            color: #D9B96F;
            background: rgba(196, 154, 74, 0.09);

            border:
                1px solid rgba(196, 154, 74, 0.25);

            border-radius: 11px;

            font-size: 0.8rem;
            font-weight: 850;
        }

        .vv-record-information {
            min-width: 0;
            flex: 1;
        }

        .vv-record-type {
            color: #7E8DA1;

            font-size: 0.67rem;
            font-weight: 750;
            letter-spacing: 0.07em;
            text-transform: uppercase;
        }

        .vv-record-name {
            margin-top: 0.12rem;

            color: #EEF2F7;

            font-size: 1.15rem;
            font-weight: 750;
            line-height: 1.3;

            overflow-wrap: anywhere;
        }

        .vv-record-meta {
            margin-top: 0.18rem;

            color: #8795A8;

            font-size: 0.74rem;
            line-height: 1.4;

            overflow-wrap: anywhere;
        }

        .vv-record-status {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;

            margin-top: 0.42rem;

            color: #AEBACA;

            font-size: 0.69rem;
            font-weight: 650;
        }

        .vv-status-dot {
            width: 5px;
            height: 5px;

            background: #C49A4A;
            border-radius: 50%;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.vv-section-marker) {
            margin-bottom: 0.9rem;

            background: rgba(8, 20, 36, 0.92);

            border:
                1px solid rgba(148, 163, 184, 0.14) !important;

            border-radius: 14px !important;

            transition: border-color 150ms ease;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.vv-section-marker):hover {
            border-color:
                rgba(148, 163, 184, 0.23) !important;
        }

        .vv-section-heading {
            display: flex;
            align-items: flex-start;
            gap: 0.72rem;

            margin-bottom: 0.85rem;
            padding-bottom: 0.75rem;

            border-bottom:
                1px solid rgba(148, 163, 184, 0.10);
        }

        .vv-section-number {
            width: 25px;
            height: 25px;
            flex: 0 0 25px;

            display: flex;
            align-items: center;
            justify-content: center;

            color: #CDAA5F;
            background: rgba(196, 154, 74, 0.08);

            border:
                1px solid rgba(196, 154, 74, 0.20);

            border-radius: 7px;

            font-size: 0.62rem;
            font-weight: 800;
        }

        .vv-section-title {
            color: #DDE5EF;

            font-size: 0.87rem;
            font-weight: 720;
        }

        .vv-section-description {
            margin-top: 0.13rem;

            color: #718095;

            font-size: 0.69rem;
            line-height: 1.35;
        }

        .vv-field {
            min-height: 68px;

            padding: 0.72rem 0.8rem;

            background: rgba(5, 13, 24, 0.55);

            border:
                1px solid rgba(148, 163, 184, 0.10);

            border-radius: 9px;
        }

        .vv-field-label {
            margin-bottom: 0.27rem;

            color: #708096;

            font-size: 0.62rem;
            font-weight: 800;
            letter-spacing: 0.07em;
            text-transform: uppercase;
        }

        .vv-field-value {
            color: #DCE4EE;

            font-size: 0.81rem;
            font-weight: 620;
            line-height: 1.42;

            overflow-wrap: anywhere;
            white-space: normal;
        }

        .vv-field-value-highlight {
            color: #D9BA73;
        }

        .vv-field-value a {
            color: #C7D3E1;
            text-decoration: none;
        }

        .vv-field-value a:hover {
            color: #D9BA73;
            text-decoration: underline;
        }

        .vv-field-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.42rem;

            color: #C5CFDB;

            font-size: 0.78rem;
            font-weight: 650;
        }

        .vv-field-badge-dot {
            width: 5px;
            height: 5px;

            background: #C49A4A;
            border-radius: 50%;
        }

        .vv-empty-state {
            padding: 1.15rem 1.25rem;

            color: #8391A3;
            background: rgba(8, 20, 36, 0.72);

            border:
                1px solid rgba(148, 163, 184, 0.13);

            border-radius: 12px;

            font-size: 0.8rem;
            line-height: 1.45;
            text-align: center;
        }

        @media (max-width: 900px) {
            [data-testid="stMainBlockContainer"]:has(.vv-page-marker) {
                padding-right: 1rem;
                padding-left: 1rem;
            }

            .vv-title {
                font-size: 1.65rem;
            }
        }
        </style>
        """
    )