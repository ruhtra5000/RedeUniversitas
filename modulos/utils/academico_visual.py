from contextlib import contextmanager
from html import escape
from typing import Iterator
import streamlit as st

# Função para marcar a página com um marcador invisível, permitindo a aplicação de estilos específicos para a página.
def marcarPagina():
    aplicarEstiloPagina()
    st.html('<span class="pv-page-marker"></span>')

# Função para marcar métricas na página com um marcador invisível, permitindo a aplicação de estilos específicos para as métricas.
def marcarMetricasPagina():
    st.html('<span class="pv-metrics-marker"></span>')

# Função para marcar uma tabela na página com um marcador invisível, permitindo a aplicação de estilos específicos para a tabela.
def marcarTabelaPagina():
    st.html('<span class="pv-table-marker"></span>')

# Função para marcar ações na página com um marcador invisível, permitindo a aplicação de estilos específicos para as ações.
def marcarAcoesPagina():
    st.html('<span class="pv-actions-marker"></span>')

# Função para marcar um painel na página com um marcador invisível, permitindo a aplicação de estilos específicos para o painel.
def marcarPainelPagina():
    st.html('<span class="pv-panel-marker"></span>')

# Função para renderizar o topo da página com título, descrição e categoria.
def renderizarTopoPagina(titulo: str, descricao: str, categoria: str):
    marcarPagina()

    st.html(f"""
        <header class="pv-header">
            <div class="pv-eyebrow">{escape(categoria)}</div>
            <h1 class="pv-title">{escape(titulo)}</h1>
            <p class="pv-description">{escape(descricao)}</p>
        </header>
        """)

# Context manager para criar um painel na página com título, descrição e contexto. O conteúdo do painel é definido dentro do bloco `with`.
@contextmanager
def painelPagina(titulo: str, descricao: str, contexto: str = "PAINEL") -> Iterator[None]:
    with st.container(border=True):
        marcarPainelPagina()

        st.html(f"""
            <div class="pv-panel-heading">
                <div>
                    <div class="pv-panel-kicker">{escape(contexto)}</div>
                    <div class="pv-panel-title">{escape(titulo)}</div>
                    <div class="pv-panel-description">
                        {escape(descricao)}
                    </div>
                </div>
            </div>
            """)

        yield

# Função para renderizar uma seção na página com número, título e descrição.
def renderizarSecaoPagina(numero: int, titulo: str, descricao: str):
    st.html(f"""
        <div class="pv-section-heading">
            <div class="pv-section-number">{numero:02d}</div>
            <div>
                <div class="pv-section-title">{escape(titulo)}</div>
                <div class="pv-section-description">
                    {escape(descricao)}
                </div>
            </div>
        </div>
        """)

# Função para renderizar um divisor de página, que é uma linha horizontal separando seções ou elementos na página.
def renderizarDivisorPagina():
    st.html('<div class="pv-divider"></div>')

# Função para renderizar o status da página com um rótulo e valor, exibindo um ponto de status colorido ao lado do rótulo.
def renderizarStatusPagina(rotulo: str, valor: str):
    st.html(f"""
        <div class="pv-status">
            <span class="pv-status-dot"></span>
            <div>
                <div class="pv-status-label">{escape(rotulo)}</div>
                <div class="pv-status-value">{escape(valor)}</div>
            </div>
        </div>
        """)

# Função para aplicar o estilo CSS personalizado nas páginas acadêmicas.
def aplicarEstiloPagina():
    st.html("""
        <style>
        [data-testid="stMainBlockContainer"]:has(.pv-page-marker) {
            width: 100%;
            max-width: 1180px !important;
            margin-right: auto !important;
            margin-left: auto !important;
            padding-top: 4.25rem !important;
            padding-right: 2.5rem !important;
            padding-bottom: 4rem !important;
            padding-left: 2.5rem !important;
        }

        .pv-page-marker,
        .pv-panel-marker,
        .pv-metrics-marker,
        .pv-actions-marker,
        .pv-table-marker {
            display: none;
        }

        [data-testid="stElementContainer"]:has(.pv-page-marker),
        [data-testid="stElementContainer"]:has(.pv-panel-marker),
        [data-testid="stElementContainer"]:has(.pv-metrics-marker),
        [data-testid="stElementContainer"]:has(.pv-actions-marker),
        [data-testid="stElementContainer"]:has(.pv-table-marker) {
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        div[data-testid="InputInstructions"] {
            display: none !important;
        }

        .pv-header {
            position: relative;
            margin: 0.25rem 0 1.45rem;
            padding: 0 0 1.2rem 1.05rem;
            border-bottom: 1px solid rgba(148, 163, 184, 0.13);
        }

        .pv-header::before {
            content: "";
            position: absolute;
            top: 0.18rem;
            bottom: 1.2rem;
            left: 0;
            width: 3px;
            background: #C49A4A;
            border-radius: 999px;
        }

        .pv-eyebrow,
        .pv-panel-kicker,
        .pv-section-kicker {
            color: #8190A4;
            font-size: 0.67rem;
            font-weight: 800;
            letter-spacing: 0.11em;
            text-transform: uppercase;
        }

        .pv-title {
            margin: 0.28rem 0 0;
            color: #F4F7FB;
            font-size: 2rem;
            font-weight: 780;
            letter-spacing: -0.035em;
            line-height: 1.15;
        }

        .pv-description {
            max-width: 780px;
            margin: 0.42rem 0 0;
            color: #8D9AAC;
            font-size: 0.87rem;
            line-height: 1.45;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.pv-panel-marker) {
            margin: 0 0 1rem !important;
            background:
                linear-gradient(
                    180deg,
                    rgba(10, 23, 40, 0.98),
                    rgba(7, 18, 32, 0.98)
                ) !important;
            border: 1px solid rgba(148, 163, 184, 0.16) !important;
            border-radius: 14px !important;
            box-shadow: 0 16px 45px rgba(0, 0, 0, 0.14) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.pv-panel-marker)
        > div {
            padding: 1.15rem 1.25rem 1.25rem !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.pv-panel-marker)
        [data-testid="stVerticalBlock"] {
            gap: 0.82rem !important;
        }

        .pv-panel-heading {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1rem;
            padding-bottom: 0.95rem;
            border-bottom: 1px solid rgba(148, 163, 184, 0.11);
        }

        .pv-panel-title {
            margin-top: 0.17rem;
            color: #DDE5EF;
            font-size: 0.94rem;
            font-weight: 730;
        }

        .pv-panel-description {
            max-width: 760px;
            margin-top: 0.2rem;
            color: #77869A;
            font-size: 0.71rem;
            line-height: 1.42;
        }

        .pv-section-heading {
            display: flex;
            align-items: flex-start;
            gap: 0.65rem;
            margin: 0.15rem 0 0.05rem;
        }

        .pv-section-number {
            display: flex;
            align-items: center;
            justify-content: center;
            flex: 0 0 auto;
            width: 26px;
            height: 26px;
            color: #D9BA73;
            background: rgba(196, 154, 74, 0.07);
            border: 1px solid rgba(196, 154, 74, 0.22);
            border-radius: 7px;
            font-size: 0.62rem;
            font-weight: 800;
        }

        .pv-section-title {
            color: #D9E2EC;
            font-size: 0.82rem;
            font-weight: 710;
            line-height: 1.3;
        }

        .pv-section-description {
            margin-top: 0.12rem;
            color: #718096;
            font-size: 0.68rem;
            line-height: 1.38;
        }

        .pv-divider {
            height: 1px;
            margin: 0.25rem 0 0.1rem;
            background: rgba(148, 163, 184, 0.10);
        }

        .pv-status {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            padding: 0.75rem 0.85rem;
            background: rgba(5, 13, 24, 0.58);
            border: 1px solid rgba(148, 163, 184, 0.13);
            border-radius: 10px;
        }

        .pv-status-dot {
            flex: 0 0 auto;
            width: 7px;
            height: 7px;
            background: #C49A4A;
            border-radius: 50%;
            box-shadow: 0 0 0 4px rgba(196, 154, 74, 0.08);
        }

        .pv-status-label {
            color: #718096;
            font-size: 0.61rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .pv-status-value {
            margin-top: 0.1rem;
            color: #DCE4EE;
            font-size: 0.79rem;
            font-weight: 680;
        }

        [data-testid="stHorizontalBlock"]:has(.pv-metrics-marker)
        [data-testid="stMetric"] {
            min-height: 96px;
            padding: 0.85rem 0.95rem;
            background: rgba(5, 13, 24, 0.55);
            border: 1px solid rgba(148, 163, 184, 0.14);
            border-top: 2px solid rgba(196, 154, 74, 0.55);
            border-radius: 11px;
        }

        [data-testid="stHorizontalBlock"]:has(.pv-metrics-marker)
        [data-testid="stMetricLabel"] p {
            color: #8291A5 !important;
            font-size: 0.67rem !important;
            font-weight: 760 !important;
        }

        [data-testid="stHorizontalBlock"]:has(.pv-metrics-marker)
        [data-testid="stMetricValue"] {
            color: #F0F4F9 !important;
            font-size: 1.35rem !important;
            font-weight: 760 !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.pv-panel-marker)
        [data-testid="stWidgetLabel"] p {
            color: #8291A5 !important;
            font-size: 0.68rem !important;
            font-weight: 760 !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.pv-panel-marker)
        [data-baseweb="base-input"],
        [data-testid="stVerticalBlockBorderWrapper"]:has(.pv-panel-marker)
        [data-baseweb="input"] > div,
        [data-testid="stVerticalBlockBorderWrapper"]:has(.pv-panel-marker)
        [data-baseweb="select"] > div {
            min-height: 41px !important;
            color: #DCE4EE !important;
            background: rgba(5, 13, 24, 0.82) !important;
            border-color: rgba(148, 163, 184, 0.17) !important;
            border-radius: 9px !important;
            box-shadow: none !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.pv-panel-marker)
        input,
        [data-testid="stVerticalBlockBorderWrapper"]:has(.pv-panel-marker)
        textarea,
        [data-testid="stVerticalBlockBorderWrapper"]:has(.pv-panel-marker)
        [data-baseweb="select"] span {
            color: #DCE4EE !important;
            font-size: 0.79rem !important;
            -webkit-text-fill-color: #DCE4EE !important;
        }

        [data-baseweb="popover"] ul {
            background: #091426 !important;
            border: 1px solid rgba(148, 163, 184, 0.18) !important;
            border-radius: 9px !important;
        }

        [data-baseweb="popover"] li:hover {
            background: rgba(196, 154, 74, 0.09) !important;
        }

        [data-testid="stTabs"] [data-baseweb="tab-list"] {
            gap: 0.35rem;
            padding: 0.3rem;
            background: rgba(7, 18, 32, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.13);
            border-radius: 10px;
        }

        [data-testid="stTabs"] [data-baseweb="tab"] {
            min-height: 38px;
            color: #8D9AAC !important;
            border-radius: 7px;
            font-size: 0.75rem;
            font-weight: 680;
        }

        [data-testid="stTabs"] [aria-selected="true"] {
            color: #E4C77F !important;
            background: rgba(196, 154, 74, 0.09) !important;
        }

        [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
            background: #C49A4A !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.pv-panel-marker)
        [data-testid="stDataFrame"],
        [data-testid="stVerticalBlockBorderWrapper"]:has(.pv-panel-marker)
        [data-testid="stDataEditor"] {
            overflow: hidden;
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 10px;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.pv-panel-marker)
        [data-testid="stBaseButton-primary"] {
            min-height: 42px !important;
            color: #E8EEF6 !important;
            background: linear-gradient(135deg, #12325A, #0B2340) !important;
            border: 1px solid rgba(107, 139, 177, 0.42) !important;
            border-radius: 9px !important;
            font-size: 0.77rem !important;
            font-weight: 720 !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.pv-panel-marker)
        [data-testid="stBaseButton-primary"]:hover {
            color: #F1D591 !important;
            border-color: rgba(196, 154, 74, 0.52) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.pv-panel-marker)
        [data-testid="stBaseButton-secondary"] {
            min-height: 42px !important;
            color: #C7D3E1 !important;
            background: rgba(10, 25, 43, 0.92) !important;
            border: 1px solid rgba(103, 132, 166, 0.34) !important;
            border-radius: 9px !important;
            font-size: 0.77rem !important;
            font-weight: 680 !important;
        }

        [data-testid="stAlert"] {
            border-radius: 10px !important;
        }

        div[role="dialog"] {
            background: #081524 !important;
            border: 1px solid rgba(148, 163, 184, 0.18) !important;
            border-radius: 14px !important;
        }

        @media (max-width: 900px) {
            [data-testid="stMainBlockContainer"]:has(.pv-page-marker) {
                padding-right: 1rem !important;
                padding-left: 1rem !important;
            }

            .pv-title {
                font-size: 1.65rem;
            }

        }
        </style>
        """)
