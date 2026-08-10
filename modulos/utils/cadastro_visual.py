from contextlib import contextmanager
from html import escape
from typing import Callable, Iterator
import streamlit as st

# Função para renderizar o topo do cadastro com título, descrição e botões de ação
def renderizarTopoCadastro(titulo: str, descricao: str, aoVoltar: Callable[[], None], prefixoChave: str, categoria: str = "CADASTRO", rotuloAcao: str | None = None, iconeAcao: str | None = None, aoAcao: Callable[[], None] | None = None):
    aplicarEstiloCadastro()

    st.html('<span class="cv-page-marker"></span>')

    if rotuloAcao and aoAcao:
        colVoltar, _, colAcao = st.columns([1.05, 4.9, 1.05])
    else:
        colVoltar, _ = st.columns([1.05, 5.95])

    with colVoltar:
        st.html('<span class="cv-nav-marker"></span>')

        if st.button(
            "Voltar",
            icon=":material/arrow_back:",
            key=f"{prefixoChave}_voltar",
            width="stretch",
        ):
            aoVoltar()

    if rotuloAcao and aoAcao:
        with colAcao:
            if st.button(
                rotuloAcao,
                icon=iconeAcao,
                key=f"{prefixoChave}_acao",
                width="stretch",
            ):
                aoAcao()

    st.html(f"""
        <header class="cv-header">
            <div class="cv-eyebrow">{escape(categoria)}</div>
            <h1 class="cv-title">{escape(titulo)}</h1>
            <p class="cv-description">{escape(descricao)}</p>
        </header>
        """)

# Função para marcar o formulário de cadastro com um marcador visual
def marcarFormularioCadastro():
    st.html('<span class="cv-form-marker"></span>')

# Função para marcar o painel de cadastro com um marcador visual
def marcarPainelCadastro():
    st.html('<span class="cv-panel-marker"></span>')

# Função para renderizar o cabeçalho do formulário de cadastro com título, descrição e contexto
def renderizarCabecalhoFormulario(titulo: str, descricao: str, contexto: str = "NOVO REGISTRO"):
    st.html(f"""
        <div class="cv-form-heading">
            <div>
                <div class="cv-form-kicker">{escape(contexto)}</div>
                <div class="cv-form-title">{escape(titulo)}</div>
                <div class="cv-form-description">
                    {escape(descricao)}
                </div>
            </div>

            <div class="cv-required-badge">
                <span class="cv-required-dot"></span>
                Campos com * são obrigatórios
            </div>
        </div>
        """)

# Context manager para criar o painel visual único usado por todos os cadastros
@contextmanager
def painelCadastro(titulo: str, descricao: str, contexto: str = "NOVO REGISTRO") -> Iterator[None]:
    """Cria o painel visual único usado por todos os cadastros."""

    with st.container(border=True):
        marcarPainelCadastro()

        renderizarCabecalhoFormulario(
            titulo=titulo,
            descricao=descricao,
            contexto=contexto,
        )

        yield

# Função para renderizar uma seção do formulário de cadastro com número, título e descrição
def renderizarSecaoCadastro(numero: int, titulo: str, descricao: str):
    st.html(f"""
        <div class="cv-section-heading">
            <div class="cv-section-number">{numero:02d}</div>
            <div>
                <div class="cv-section-title">
                    {escape(titulo)}
                </div>
                <div class="cv-section-description">
                    {escape(descricao)}
                </div>
            </div>
        </div>
        """)

# Função para renderizar um divisor visual entre seções do formulário de cadastro
def renderizarDivisorCadastro():
    st.html('<div class="cv-divider"></div>')

# Função para marcar as ações do formulário de cadastro com um marcador visual
def marcarAcoesCadastro():
    st.html('<span class="cv-actions-marker"></span>')

# Função para renderizar o botão de ação principal do formulário de cadastro com rótulo, ícone e chave
def renderizarBotaoCadastro(rotulo: str, icone: str, chave: str, desabilitado: bool = False) -> bool:
    """Renderiza a ação principal sempre com a mesma largura e posição."""

    _, colunaCentral, _ = st.columns([2, 3, 2])

    with colunaCentral:
        marcarAcoesCadastro()

        return st.button(
            rotulo,
            icon=icone,
            key=chave,
            type="primary",
            width="stretch",
            disabled=desabilitado,
        )

# Função para renderizar um aviso de cadastro com título e descrição
def renderizarAvisoCadastro(titulo: str, descricao: str):
    st.html(f"""
        <div class="cv-alert">
            <div class="cv-alert-icon">!</div>
            <div>
                <div class="cv-alert-title">{escape(titulo)}</div>
                <div class="cv-alert-description">
                    {escape(descricao)}
                </div>
            </div>
        </div>
        """)
    
# Função para aplicar o estilo CSS personalizado nos campos de entrada bloqueados
def aplicarEstiloCamposBloqueados():
    st.html(
        """
        <style>

        div[data-testid="stTextInput"]:has(input:disabled)
        div[data-testid="stTextInputRootElement"] {
            background-color: #132A3A !important;
            border-color: #31506A !important;
        }

        div[data-testid="stTextInput"]
        input[data-testid="stTextInputField"]:disabled {
            color: #9FBAD0 !important;
            -webkit-text-fill-color: #9FBAD0 !important;
            opacity: 1 !important;
            cursor: not-allowed !important;
        }
        </style>
        """
    )

# Função para aplicar o estilo CSS personalizado na página inicial
def aplicarEstiloCadastro():
    st.html("""
        <style>
        [data-testid="stMainBlockContainer"]:has(.cv-page-marker) {
            width: 100%;
            max-width: 1080px !important;

            margin-right: auto !important;
            margin-left: auto !important;

            padding-top: 4.25rem !important;
            padding-right: 2.5rem !important;
            padding-bottom: 4rem !important;
            padding-left: 2.5rem !important;
        }

        .cv-page-marker,
        .cv-nav-marker,
        .cv-form-marker,
        .cv-panel-marker,
        .cv-actions-marker {
            display: none;
        }

        [data-testid="stElementContainer"]:has(.cv-page-marker),
        [data-testid="stElementContainer"]:has(.cv-nav-marker),
        [data-testid="stElementContainer"]:has(.cv-form-marker),
        [data-testid="stElementContainer"]:has(.cv-panel-marker),
        [data-testid="stElementContainer"]:has(.cv-actions-marker) {
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        div[data-testid="InputInstructions"] {
            display: none !important;
        }

        [data-testid="stHorizontalBlock"]:has(.cv-nav-marker) {
            margin-bottom: 0.7rem;
        }

        [data-testid="stHorizontalBlock"]:has(.cv-nav-marker)
        [data-testid="stBaseButton-secondary"] {
            min-height: 40px;

            color: #C7D3E1 !important;
            background: rgba(10, 25, 43, 0.92) !important;

            border:
                1px solid rgba(103, 132, 166, 0.34) !important;

            border-radius: 9px !important;

            font-size: 0.78rem !important;
            font-weight: 650 !important;
        }

        [data-testid="stHorizontalBlock"]:has(.cv-nav-marker)
        [data-testid="stBaseButton-secondary"]:hover {
            color: #E2C57F !important;
            background: rgba(16, 37, 62, 0.98) !important;
            border-color: rgba(196, 154, 74, 0.48) !important;
        }

        .cv-header {
            position: relative;

            margin: 0.6rem 0 1.25rem;
            padding: 0 0 1.2rem 1.05rem;

            border-bottom:
                1px solid rgba(148, 163, 184, 0.13);
        }

        .cv-header::before {
            content: "";

            position: absolute;
            top: 0.18rem;
            bottom: 1.2rem;
            left: 0;

            width: 3px;

            background: #C49A4A;
            border-radius: 999px;
        }

        .cv-eyebrow {
            margin-bottom: 0.3rem;

            color: #8190A4;

            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .cv-title {
            margin: 0;

            color: #F4F7FB;

            font-size: 2rem;
            font-weight: 780;
            letter-spacing: -0.035em;
            line-height: 1.15;
        }

        .cv-description {
            max-width: 760px;

            margin: 0.42rem 0 0;

            color: #8D9AAC;

            font-size: 0.87rem;
            line-height: 1.45;
        }

        .cv-alert {
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;

            margin-bottom: 1rem;
            padding: 0.85rem 1rem;

            background: rgba(196, 154, 74, 0.06);

            border:
                1px solid rgba(196, 154, 74, 0.22);

            border-radius: 11px;
        }

        .cv-alert-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            flex: 0 0 auto;

            width: 26px;
            height: 26px;

            color: #D9BA73;
            background: rgba(196, 154, 74, 0.09);

            border:
                1px solid rgba(196, 154, 74, 0.22);

            border-radius: 7px;

            font-size: 0.76rem;
            font-weight: 800;
        }

        .cv-alert-title {
            color: #D7DEE8;

            font-size: 0.79rem;
            font-weight: 720;
        }

        .cv-alert-description {
            margin-top: 0.13rem;

            color: #8795A7;

            font-size: 0.71rem;
            line-height: 1.42;
        }

        [data-testid="stForm"]:has(.cv-form-marker) {
            margin: 0 !important;
            padding: 1.15rem 1.25rem 1.25rem !important;

            background:
                linear-gradient(
                    180deg,
                    rgba(10, 23, 40, 0.98),
                    rgba(7, 18, 32, 0.98)
                ) !important;

            border:
                1px solid rgba(148, 163, 184, 0.16) !important;

            border-radius: 14px !important;

            box-shadow:
                0 16px 45px rgba(0, 0, 0, 0.16) !important;
        }

        [data-testid="stForm"]:has(.cv-form-marker)
        > [data-testid="stVerticalBlock"] {
            gap: 0.85rem !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker) {
            margin: 0 !important;

            background:
                linear-gradient(
                    180deg,
                    rgba(10, 23, 40, 0.98),
                    rgba(7, 18, 32, 0.98)
                ) !important;

            border:
                1px solid rgba(148, 163, 184, 0.16) !important;

            border-radius: 14px !important;

            box-shadow:
                0 16px 45px rgba(0, 0, 0, 0.16) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        > div {
            padding: 1.15rem 1.25rem 1.25rem !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        [data-testid="stVerticalBlock"] {
            gap: 0.85rem !important;
        }

        .cv-form-heading {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;

            padding-bottom: 0.95rem;

            border-bottom:
                1px solid rgba(148, 163, 184, 0.11);
        }

        .cv-form-kicker {
            margin-bottom: 0.17rem;

            color: #708096;

            font-size: 0.61rem;
            font-weight: 800;
            letter-spacing: 0.09em;
            text-transform: uppercase;
        }

        .cv-form-title {
            color: #DDE5EF;

            font-size: 0.91rem;
            font-weight: 720;
        }

        .cv-form-description {
            margin-top: 0.18rem;

            color: #77869A;

            font-size: 0.71rem;
            line-height: 1.42;
        }

        .cv-required-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.42rem;
            flex: 0 0 auto;

            padding: 0.4rem 0.62rem;

            color: #9EABBA;
            background: rgba(5, 13, 24, 0.58);

            border:
                1px solid rgba(148, 163, 184, 0.13);

            border-radius: 8px;

            font-size: 0.65rem;
            font-weight: 650;
        }

        .cv-required-dot {
            width: 5px;
            height: 5px;

            background: #C49A4A;
            border-radius: 50%;
        }

        .cv-section-heading {
            display: flex;
            align-items: flex-start;
            gap: 0.65rem;

            margin: 0.15rem 0 0.05rem;
        }

        .cv-section-number {
            display: flex;
            align-items: center;
            justify-content: center;
            flex: 0 0 auto;

            width: 26px;
            height: 26px;

            color: #D9BA73;
            background: rgba(196, 154, 74, 0.07);

            border:
                1px solid rgba(196, 154, 74, 0.22);

            border-radius: 7px;

            font-size: 0.62rem;
            font-weight: 800;
        }

        .cv-section-title {
            color: #D9E2EC;

            font-size: 0.82rem;
            font-weight: 710;
            line-height: 1.3;
        }

        .cv-section-description {
            margin-top: 0.12rem;

            color: #718096;

            font-size: 0.68rem;
            line-height: 1.38;
        }

        .cv-divider {
            height: 1px;

            margin: 0.25rem 0 0.1rem;

            background: rgba(148, 163, 184, 0.10);
        }

        [data-testid="stForm"]:has(.cv-form-marker)
        [data-testid="stWidgetLabel"] p,
        [data-testid="stForm"]:has(.cv-form-marker)
        [data-testid="stTextInput"] label p,
        [data-testid="stForm"]:has(.cv-form-marker)
        [data-testid="stSelectbox"] label p,
        [data-testid="stForm"]:has(.cv-form-marker)
        [data-testid="stNumberInput"] label p,
        [data-testid="stForm"]:has(.cv-form-marker)
        [data-testid="stDateInput"] label p {
            color: #8291A5 !important;

            font-size: 0.68rem !important;
            font-weight: 760 !important;
            letter-spacing: 0.025em !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        [data-testid="stWidgetLabel"] p,
        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        [data-testid="stTextInput"] label p,
        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        [data-testid="stSelectbox"] label p,
        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        [data-testid="stNumberInput"] label p,
        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        [data-testid="stDateInput"] label p {
            color: #8291A5 !important;

            font-size: 0.68rem !important;
            font-weight: 760 !important;
            letter-spacing: 0.025em !important;
        }

        [data-testid="stForm"]:has(.cv-form-marker)
        [data-baseweb="base-input"],
        [data-testid="stForm"]:has(.cv-form-marker)
        [data-baseweb="input"] > div {
            min-height: 41px !important;

            color: #DCE4EE !important;
            background: rgba(5, 13, 24, 0.82) !important;

            border-color:
                rgba(148, 163, 184, 0.17) !important;

            border-radius: 9px !important;

            box-shadow: none !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        [data-baseweb="base-input"],
        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        [data-baseweb="input"] > div {
            min-height: 41px !important;

            color: #DCE4EE !important;
            background: rgba(5, 13, 24, 0.82) !important;

            border-color:
                rgba(148, 163, 184, 0.17) !important;

            border-radius: 9px !important;

            box-shadow: none !important;
        }

        [data-testid="stForm"]:has(.cv-form-marker)
        [data-baseweb="base-input"]:focus-within,
        [data-testid="stForm"]:has(.cv-form-marker)
        [data-baseweb="input"]:focus-within > div {
            border-color:
                rgba(196, 154, 74, 0.50) !important;

            box-shadow:
                0 0 0 2px rgba(196, 154, 74, 0.08) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        [data-baseweb="base-input"]:focus-within,
        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        [data-baseweb="input"]:focus-within > div {
            border-color:
                rgba(196, 154, 74, 0.50) !important;

            box-shadow:
                0 0 0 2px rgba(196, 154, 74, 0.08) !important;
        }

        [data-testid="stForm"]:has(.cv-form-marker) input,
        [data-testid="stForm"]:has(.cv-form-marker) textarea {
            color: #DCE4EE !important;
            background: transparent !important;

            font-size: 0.79rem !important;

            -webkit-text-fill-color: #DCE4EE !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        input,
        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        textarea {
            color: #DCE4EE !important;
            background: transparent !important;

            font-size: 0.79rem !important;

            -webkit-text-fill-color: #DCE4EE !important;
        }

        [data-testid="stForm"]:has(.cv-form-marker)
        input::placeholder,
        [data-testid="stForm"]:has(.cv-form-marker)
        textarea::placeholder {
            color: #5F6E82 !important;
            opacity: 1 !important;

            -webkit-text-fill-color: #5F6E82 !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        input::placeholder,
        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        textarea::placeholder {
            color: #5F6E82 !important;
            opacity: 1 !important;

            -webkit-text-fill-color: #5F6E82 !important;
        }

        [data-testid="stForm"]:has(.cv-form-marker)
        [data-baseweb="select"] > div {
            min-height: 41px !important;

            color: #DCE4EE !important;
            background: rgba(5, 13, 24, 0.82) !important;

            border:
                1px solid rgba(148, 163, 184, 0.17) !important;

            border-radius: 9px !important;

            box-shadow: none !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        [data-baseweb="select"] > div {
            min-height: 41px !important;

            color: #DCE4EE !important;
            background: rgba(5, 13, 24, 0.82) !important;

            border:
                1px solid rgba(148, 163, 184, 0.17) !important;

            border-radius: 9px !important;

            box-shadow: none !important;
        }

        [data-testid="stForm"]:has(.cv-form-marker)
        [data-baseweb="select"]:focus-within > div {
            border-color:
                rgba(196, 154, 74, 0.50) !important;

            box-shadow:
                0 0 0 2px rgba(196, 154, 74, 0.08) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        [data-baseweb="select"]:focus-within > div {
            border-color:
                rgba(196, 154, 74, 0.50) !important;

            box-shadow:
                0 0 0 2px rgba(196, 154, 74, 0.08) !important;
        }

        [data-testid="stForm"]:has(.cv-form-marker)
        [data-baseweb="select"] span {
            color: #C9D3DF !important;

            font-size: 0.79rem !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        [data-baseweb="select"] span {
            color: #C9D3DF !important;

            font-size: 0.79rem !important;
        }

        [data-baseweb="popover"] {
            color: #DCE4EE !important;
        }

        [data-baseweb="popover"] ul {
            background: #091426 !important;

            border:
                1px solid rgba(148, 163, 184, 0.18) !important;

            border-radius: 9px !important;
        }

        [data-baseweb="popover"] li:hover {
            background: rgba(196, 154, 74, 0.09) !important;
        }

        [data-testid="stForm"]:has(.cv-form-marker)
        [aria-disabled="true"] {
            opacity: 0.5 !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        [aria-disabled="true"] {
            opacity: 0.5 !important;
        }

        [data-testid="stForm"]:has(.cv-form-marker)
        [data-testid="stCheckbox"] p,
        [data-testid="stForm"]:has(.cv-form-marker)
        [data-testid="stRadio"] p,
        [data-testid="stForm"]:has(.cv-form-marker)
        [data-testid="stToggle"] p {
            color: #AEB9C7 !important;

            font-size: 0.76rem !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        [data-testid="stCheckbox"] p,
        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        [data-testid="stRadio"] p,
        [data-testid="stVerticalBlockBorderWrapper"]:has(.cv-panel-marker)
        [data-testid="stToggle"] p {
            color: #AEB9C7 !important;

            font-size: 0.76rem !important;
        }

        [data-testid="stHorizontalBlock"]:has(.cv-actions-marker) {
            margin-top: 0.25rem;
        }

        [data-testid="stHorizontalBlock"]:has(.cv-actions-marker)
        [data-testid="stFormSubmitButton"] button,
        [data-testid="stHorizontalBlock"]:has(.cv-actions-marker)
        [data-testid="stBaseButton-primaryFormSubmit"],
        [data-testid="stHorizontalBlock"]:has(.cv-actions-marker)
        button[kind="primaryFormSubmit"] {
            min-height: 43px !important;

            color: #E8EEF6 !important;
            background:
                linear-gradient(
                    135deg,
                    rgba(18, 50, 90, 1),
                    rgba(11, 35, 64, 1)
                ) !important;

            border:
                1px solid rgba(107, 139, 177, 0.42) !important;

            border-radius: 9px !important;

            box-shadow:
                0 9px 24px rgba(0, 0, 0, 0.16) !important;

            font-size: 0.79rem !important;
            font-weight: 720 !important;
        }

        [data-testid="stHorizontalBlock"]:has(.cv-actions-marker)
        [data-testid="stFormSubmitButton"] button:hover,
        [data-testid="stHorizontalBlock"]:has(.cv-actions-marker)
        [data-testid="stBaseButton-primaryFormSubmit"]:hover,
        [data-testid="stHorizontalBlock"]:has(.cv-actions-marker)
        button[kind="primaryFormSubmit"]:hover {
            color: #F1D591 !important;
            background:
                linear-gradient(
                    135deg,
                    rgba(22, 59, 103, 1),
                    rgba(13, 41, 73, 1)
                ) !important;

            border-color: rgba(196, 154, 74, 0.52) !important;
        }

        [data-testid="stHorizontalBlock"]:has(.cv-actions-marker)
        [data-testid="stBaseButton-primary"],
        [data-testid="stHorizontalBlock"]:has(.cv-actions-marker)
        button[kind="primary"] {
            min-height: 43px !important;

            color: #E8EEF6 !important;
            background:
                linear-gradient(
                    135deg,
                    rgba(18, 50, 90, 1),
                    rgba(11, 35, 64, 1)
                ) !important;

            border:
                1px solid rgba(107, 139, 177, 0.42) !important;

            border-radius: 9px !important;

            box-shadow:
                0 9px 24px rgba(0, 0, 0, 0.16) !important;

            font-size: 0.79rem !important;
            font-weight: 720 !important;
        }

        [data-testid="stHorizontalBlock"]:has(.cv-actions-marker)
        [data-testid="stBaseButton-primary"]:hover,
        [data-testid="stHorizontalBlock"]:has(.cv-actions-marker)
        button[kind="primary"]:hover {
            color: #F1D591 !important;
            background:
                linear-gradient(
                    135deg,
                    rgba(22, 59, 103, 1),
                    rgba(13, 41, 73, 1)
                ) !important;

            border-color: rgba(196, 154, 74, 0.52) !important;
        }

        [data-testid="stMainBlockContainer"]:has(.cv-page-marker)
        [data-testid="stAlert"] {
            border-radius: 10px !important;
        }

        @media (max-width: 900px) {
            [data-testid="stMainBlockContainer"]:has(.cv-page-marker) {
                padding-right: 1rem !important;
                padding-left: 1rem !important;
            }

            .cv-title {
                font-size: 1.65rem;
            }

            .cv-form-heading {
                align-items: flex-start;
                flex-direction: column;
            }
        }
        </style>
        """)
