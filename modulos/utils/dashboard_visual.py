from __future__ import annotations
import html
from dataclasses import dataclass
from decimal import Decimal
from typing import Any
import streamlit as st

# Classe de dados para representar uma métrica do dashboard
@dataclass(frozen=True)
class MetricaDashboard:
    rotulo: str
    valor: str
    descricao: str
    cor: str = "#C49A4A"
    sigla: str | None = None

# Classe de dados para representar um item de distribuição no dashboard
@dataclass(frozen=True)
class ItemDistribuicao:
    rotulo: str
    valor: int
    cor: str

# Função auxiliar para criar uma sigla a partir de um rótulo
def criarSigla(rotulo: str) -> str:
    palavras_ignoradas = {"DE", "DA", "DO", "DAS", "DOS", "E", "OU"}
    palavras = [
        palavra
        for palavra in rotulo.upper().replace("/", " ").split()
        if palavra not in palavras_ignoradas
    ]

    if not palavras:
        return "•"

    if len(palavras) == 1:
        return palavras[0][:2]

    return f"{palavras[0][0]}{palavras[1][0]}"

# Função para renderizar o cabeçalho do dashboard
def renderizarCabecalhoDashboard(*, titulo: str, descricao: str, prefixo_chave: str) -> bool:
    aplicarEstiloDashboard()
    st.html('<span class="ru-page-marker"></span>')

    coluna_texto, coluna_acao = st.columns(
        [6.2, 1.05],
        gap="large",
        vertical_alignment="center",
    )

    with coluna_texto:
        st.html(
            f"""
            <div class="ru-dashboard-header">
                <div class="ru-dashboard-kicker">Dashboard</div>
                <h1 class="ru-dashboard-title">{html.escape(titulo)}</h1>
                <p class="ru-dashboard-description">{html.escape(descricao)}</p>
            </div>
            """
        )

    with coluna_acao:
        atualizar = st.button(
            "Atualizar",
            icon=":material/refresh:",
            key=f"{prefixo_chave}_atualizar",
            type="secondary",
            use_container_width=True,
        )

    return atualizar

# Função para renderizar métricas no dashboard
def renderizarMetricasDashboard(metricas: list[MetricaDashboard], *, colunas: int) -> None:
    colunas = max(2, min(colunas, 4))

    cards = []

    for metrica in metricas:
        cor = html.escape(metrica.cor)
        sigla = html.escape(metrica.sigla or criarSigla(metrica.rotulo))

        cards.append(
            (
                f'<div class="ru-metric-card" style="--ru-card-color: {cor};">'
                    '<div>'
                        '<div class="ru-metric-top">'
                            '<div class="ru-metric-label">'
                                '<span class="ru-metric-dot"></span>'
                                f'{html.escape(metrica.rotulo)}'
                            '</div>'
                            f'<div class="ru-metric-badge">{sigla}</div>'
                        '</div>'
                        f'<div class="ru-metric-value">{html.escape(metrica.valor)}</div>'
                    '</div>'
                    '<div class="ru-metric-footer">'
                        f'<div class="ru-metric-description">{html.escape(metrica.descricao)}</div>'
                        '<div class="ru-metric-mini-line"></div>'
                    '</div>'
                '</div>'
            )
        )

    st.html(
        f'<div class="ru-metric-grid ru-metric-grid--{colunas}">'
        f'{"".join(cards)}'
        '</div>'
    )

# Função para criar uma seção no dashboard
def criarSecaoDashboard(*, titulo: str, descricao: str, meta: str | None = None, contexto: str = "Painel", numero: int | None = None):
    secao = st.container(border=True)
    secao.html('<span class="ru-panel-marker"></span>')

    meta_html = (
        f'<div class="ru-section-meta">{html.escape(meta)}</div>'
        if meta
        else ""
    )

    numero_exibicao = numero if numero is not None else 1
    numero_html = (
        f'<div class="ru-section-index">{numero_exibicao:02d}</div>'
    )

    secao.html(
        f"""
        <div class="ru-section-header">
            <div class="ru-section-left">
                {numero_html}
                <div>
                    <div class="ru-section-kicker">{html.escape(contexto)}</div>
                    <h2 class="ru-section-title">{html.escape(titulo)}</h2>
                    <p class="ru-section-description">{html.escape(descricao)}</p>
                </div>
            </div>
            {meta_html}
        </div>
        """
    )

    return secao

# Função interna para renderizar uma distribuição padrão no dashboard
def renderizarDistribuicaoPadrao(itens: list[ItemDistribuicao], *, sufixo_percentual: str, mensagem_vazia: str) -> None:
    total = sum(max(item.valor, 0) for item in itens)

    if total <= 0:
        renderizarEstadoVazio(mensagem_vazia)
        return

    segmentos = []
    cards = []

    for item in itens:
        valor = max(item.valor, 0)
        percentual = (valor / total) * 100
        cor = html.escape(item.cor)

        segmentos.append(
            '<div class="ru-distribution-segment" '
            f'style="width: {percentual:.4f}%; background: {cor};">'
            '</div>'
        )

        cards.append(
            f"""
            <div
                class="ru-distribution-card"
                style="--ru-item-color: {cor};"
            >
                <div class="ru-distribution-card-label">
                    <span class="ru-status-dot"></span>
                    {html.escape(item.rotulo)}
                </div>

                <div class="ru-distribution-card-value">
                    {formatarInteiro(valor)}
                    <span class="ru-distribution-card-percentage">
                        {formatarPercentual(percentual)}
                        {html.escape(sufixo_percentual)}
                    </span>
                </div>

                <div class="ru-distribution-mini-track">
                    <div
                        class="ru-distribution-mini-fill"
                        style="width: {percentual:.4f}%;">
                    </div>
                </div>
            </div>
            """
        )

    st.html(
        f"""
        <div class="ru-distribution-wrap">
            <div class="ru-distribution-track">
                {''.join(segmentos)}
            </div>

            <div class="ru-distribution-grid">
                {''.join(cards)}
            </div>
        </div>
        """
    )

# Função para renderizar a distribuição de status dos alunos no dashboard
def renderizarDistribuicaoStatus(itens: list[ItemDistribuicao]) -> None:
    renderizarDistribuicaoPadrao(
        itens,
        sufixo_percentual="dos alunos",
        mensagem_vazia="Ainda não existem alunos para apresentar.",
    )

# Função para renderizar a distribuição de desempenho dos avaliados no dashboard
def renderizarFaixasDesempenho(itens: list[ItemDistribuicao]) -> None:
    renderizarDistribuicaoPadrao(
        itens,
        sufixo_percentual="dos avaliados",
        mensagem_vazia=(
            "Ainda não existem dados de desempenho para apresentar."
        ),
    )
# Função para renderizar um estado vazio no dashboard
def renderizarEstadoVazio(mensagem: str) -> None:
    st.html(
        f'<div class="ru-empty-state">{html.escape(mensagem)}</div>'
    )

# Função para converter um valor em número, com tratamento de casos especiais
def paraNumero(valor: Any, padrao: float = 0.0) -> float:
    if valor is None:
        return padrao

    if isinstance(valor, (list, tuple)) and len(valor) == 1:
        valor = valor[0]

    if hasattr(valor, "_mapping"):
        valores = list(valor._mapping.values())
        if len(valores) == 1:
            valor = valores[0]

    if isinstance(valor, Decimal):
        return float(valor)

    try:
        return float(valor)
    except (TypeError, ValueError):
        return padrao

# Função para formatar um valor como inteiro com separador de milhar
def formatarInteiro(valor: Any) -> str:
    numero = int(round(paraNumero(valor)))
    return f"{numero:,}".replace(",", ".")

# Função para formatar um valor como decimal com separador de milhar e casas decimais
def formatarDecimal(valor: Any, casas: int = 2) -> str:
    numero = paraNumero(valor)
    texto = f"{numero:,.{casas}f}"
    return texto.replace(",", "_").replace(".", ",").replace("_", ".")

# Função para formatar um valor como percentual com casas decimais
def formatarPercentual(valor: Any, casas: int = 1) -> str:
    return f"{formatarDecimal(valor, casas)}%"

# Função para aplicar o estilo do dashboard usando CSS
def aplicarEstiloDashboard() -> None:
    st.html(
        """
        <style>
        [data-testid="stMainBlockContainer"]:has(.ru-page-marker) {
            --ru-page-gap: 1.15rem;
            --ru-panel-gap: 0.90rem;
            --ru-grid-gap: 0.72rem;

            width: 100%;
            max-width: 1180px !important;
            margin-right: auto !important;
            margin-left: auto !important;
            padding-top: 4.25rem !important;
            padding-right: 2.5rem !important;
            padding-bottom: 4rem !important;
            padding-left: 2.5rem !important;
        }

        [data-testid="stMainBlockContainer"]:has(.ru-page-marker)
        [data-testid="stVerticalBlock"] {
            gap: var(--ru-page-gap) !important;
        }

        .ru-page-marker,
        .ru-panel-marker {
            display: none;
        }

        [data-testid="stElementContainer"]:has(.ru-page-marker),
        [data-testid="stElementContainer"]:has(.ru-panel-marker) {
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        .ru-dashboard-header {
            position: relative;
            margin: 0;
            padding: 0 0 1.05rem 1.05rem;
            border-bottom: 1px solid rgba(148, 163, 184, 0.13);
        }

        .ru-dashboard-header::before {
            content: "";
            position: absolute;
            top: 0.18rem;
            bottom: 1.05rem;
            left: 0;
            width: 3px;
            background: #C49A4A;
            border-radius: 999px;
        }

        .ru-dashboard-kicker {
            color: #8190A4;
            font-size: 0.67rem;
            font-weight: 800;
            letter-spacing: 0.11em;
            line-height: 1.2;
            text-transform: uppercase;
        }

        .ru-dashboard-title {
            margin: 0.28rem 0 0;
            color: #F4F7FB;
            font-size: 2rem;
            font-weight: 780;
            letter-spacing: -0.035em;
            line-height: 1.15;
        }

        .ru-dashboard-description {
            max-width: 780px;
            margin: 0.42rem 0 0;
            color: #8D9AAC;
            font-size: 0.87rem;
            line-height: 1.45;
        }

        [data-testid="stHorizontalBlock"]:has(.ru-dashboard-header)
        [data-testid="stButton"] button {
            min-height: 42px !important;
            color: #C7D3E1 !important;
            background: rgba(10, 25, 43, 0.92) !important;
            border: 1px solid rgba(103, 132, 166, 0.34) !important;
            border-radius: 9px !important;
            font-size: 0.77rem !important;
            font-weight: 680 !important;
            box-shadow: none !important;
            transition: all 160ms ease;
        }

        [data-testid="stHorizontalBlock"]:has(.ru-dashboard-header)
        [data-testid="stButton"] button:hover {
            color: #F1D591 !important;
            border-color: rgba(196, 154, 74, 0.52) !important;
            background: rgba(12, 29, 49, 0.96) !important;
            transform: translateY(-1px);
        }

        .ru-metric-grid {
            display: grid;
            gap: var(--ru-grid-gap);
            width: 100%;
            margin: 0;
        }

        .ru-metric-grid--2 {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .ru-metric-grid--3 {
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }

        .ru-metric-grid--4 {
            grid-template-columns: repeat(4, minmax(0, 1fr));
        }

        .ru-metric-card {
            --ru-card-color: #C49A4A;

            position: relative;
            min-width: 0;
            min-height: 138px;
            overflow: hidden;

            display: flex;
            flex-direction: column;
            justify-content: space-between;

            padding: 1rem 1rem 0.95rem;

            background:
                linear-gradient(
                    180deg,
                    rgba(10, 23, 40, 0.98),
                    rgba(7, 18, 32, 0.98)
                );

            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 14px;

            box-shadow: 0 16px 45px rgba(0, 0, 0, 0.12);

            transition:
                transform 160ms ease,
                border-color 160ms ease;
        }

        .ru-metric-card:hover {
            transform: translateY(-2px);
            border-color: color-mix(
                in srgb,
                var(--ru-card-color) 34%,
                rgba(148, 163, 184, 0.18)
            );
        }

        .ru-metric-card::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background: var(--ru-card-color);
            opacity: 0.82;
        }

        .ru-metric-card::after {
            content: "";
            position: absolute;
            right: -34px;
            top: -42px;
            width: 108px;
            height: 108px;
            border-radius: 999px;
            background: var(--ru-card-color);
            opacity: 0.035;
            pointer-events: none;
        }

        .ru-metric-top {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 0.75rem;
        }

        .ru-metric-label {
            display: flex;
            align-items: center;
            min-width: 0;
            gap: 0.45rem;

            color: #8291A5;
            font-size: 0.67rem;
            font-weight: 780;
            letter-spacing: 0.04em;
            line-height: 1.25;
            text-transform: uppercase;
        }

        .ru-metric-dot {
            flex: 0 0 auto;
            width: 6px;
            height: 6px;
            border-radius: 999px;
            background: var(--ru-card-color);
            box-shadow: 0 0 0 4px color-mix(
                in srgb,
                var(--ru-card-color) 9%,
                transparent
            );
        }

        .ru-metric-badge {
            flex: 0 0 auto;

            display: flex;
            align-items: center;
            justify-content: center;

            width: 32px;
            height: 32px;

            color: color-mix(
                in srgb,
                var(--ru-card-color) 84%,
                #F4F7FB
            );

            background: color-mix(
                in srgb,
                var(--ru-card-color) 8%,
                rgba(5, 13, 24, 0.84)
            );

            border: 1px solid color-mix(
                in srgb,
                var(--ru-card-color) 22%,
                rgba(148, 163, 184, 0.12)
            );

            border-radius: 9px;

            font-size: 0.62rem;
            font-weight: 830;
            letter-spacing: 0.03em;
        }

        .ru-metric-value {
            margin: 0.63rem 0 0;
            color: #F0F4F9;
            font-size: 1.85rem;
            font-weight: 780;
            letter-spacing: -0.045em;
            line-height: 1;
        }

        .ru-metric-footer {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 0.5rem;

            margin-top: 0.72rem;
            padding-top: 0.68rem;

            border-top: 1px solid rgba(148, 163, 184, 0.09);
        }

        .ru-metric-description {
            color: #718096;
            font-size: 0.68rem;
            line-height: 1.38;
        }

        .ru-metric-mini-line {
            flex: 0 0 auto;
            width: 24px;
            height: 2px;
            margin-bottom: 0.18rem;
            border-radius: 99px;
            background: var(--ru-card-color);
            opacity: 0.75;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.ru-panel-marker) {
            margin: 0 !important;

            background:
                linear-gradient(
                    180deg,
                    rgba(10, 23, 40, 0.98),
                    rgba(7, 18, 32, 0.98)
                ) !important;

            border: 1px solid rgba(148, 163, 184, 0.16) !important;
            border-radius: 14px !important;
            box-shadow: 0 16px 45px rgba(0, 0, 0, 0.13) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.ru-panel-marker)
        > div {
            padding: 1rem !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.ru-panel-marker)
        [data-testid="stVerticalBlock"] {
            gap: var(--ru-panel-gap) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.ru-panel-marker)
        .ru-metric-grid,
        [data-testid="stVerticalBlockBorderWrapper"]:has(.ru-panel-marker)
        .ru-distribution-wrap {
            margin: 0 !important;
        }

        .ru-section-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1rem;

            padding: 0 0 0.90rem;
            margin: 0;

            border-bottom: 1px solid rgba(148, 163, 184, 0.11);
        }

        .ru-section-left {
            display: flex;
            align-items: flex-start;
            gap: 0.7rem;
            min-width: 0;
        }

        .ru-section-index {
            display: flex;
            align-items: center;
            justify-content: center;
            flex: 0 0 auto;

            width: 28px;
            height: 28px;

            color: #D9BA73;
            background: rgba(196, 154, 74, 0.07);
            border: 1px solid rgba(196, 154, 74, 0.22);
            border-radius: 7px;

            font-size: 0.60rem;
            font-weight: 820;
        }

        .ru-section-kicker {
            color: #8190A4;
            font-size: 0.61rem;
            font-weight: 800;
            letter-spacing: 0.09em;
            line-height: 1.2;
            text-transform: uppercase;
        }

        .ru-section-title {
            margin: 0.15rem 0 0;
            color: #DDE5EF;
            font-size: 0.94rem;
            font-weight: 730;
            line-height: 1.3;
        }

        .ru-section-description {
            max-width: 760px;
            margin: 0.2rem 0 0;
            color: #77869A;
            font-size: 0.71rem;
            line-height: 1.42;
        }

        .ru-section-meta {
            flex: 0 0 auto;
            align-self: center;

            padding: 0.4rem 0.62rem;

            color: #D9BA73;
            background: rgba(196, 154, 74, 0.07);
            border: 1px solid rgba(196, 154, 74, 0.20);
            border-radius: 999px;

            font-size: 0.64rem;
            font-weight: 780;
        }

        .ru-distribution-wrap {
            display: grid;
            gap: 0.86rem;
            width: 100%;
            padding: 0;
            margin: 0;
        }

        .ru-distribution-track {
            display: flex;
            width: 100%;
            height: 7px;
            overflow: hidden;

            margin: 0;

            background: rgba(5, 13, 24, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.10);
            border-radius: 999px;
        }

        .ru-distribution-segment {
            height: 100%;
            min-width: 0;
        }

        .ru-distribution-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: var(--ru-grid-gap);
            width: 100%;
        }

        .ru-distribution-card {
            --ru-item-color: #C49A4A;

            position: relative;
            min-width: 0;
            min-height: 94px;
            overflow: hidden;

            display: flex;
            flex-direction: column;

            padding: 0.80rem 0.82rem 0.72rem;

            background: rgba(5, 13, 24, 0.56);
            border: 1px solid rgba(148, 163, 184, 0.13);
            border-radius: 10px;
        }

        .ru-distribution-card::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0.78rem;
            bottom: 0.78rem;
            width: 2px;
            background: var(--ru-item-color);
            border-radius: 0 999px 999px 0;
            opacity: 0.82;
        }

        .ru-distribution-card-label {
            display: flex;
            align-items: center;
            min-width: 0;
            gap: 0.42rem;

            color: #8291A5;
            font-size: 0.66rem;
            font-weight: 700;
            line-height: 1.20;
        }

        .ru-status-dot {
            flex: 0 0 auto;
            width: 6px;
            height: 6px;
            background: var(--ru-item-color);
            border-radius: 999px;
            box-shadow: 0 0 0 3px color-mix(
                in srgb,
                var(--ru-item-color) 9%,
                transparent
            );
        }

        .ru-distribution-card-value {
            margin-top: 0.52rem;

            color: #F0F4F9;
            font-size: 1.28rem;
            font-weight: 770;
            letter-spacing: -0.035em;
            line-height: 1;
        }

        .ru-distribution-card-percentage {
            display: block;
            margin-top: 0.20rem;

            color: #718096;
            font-size: 0.63rem;
            font-weight: 600;
            line-height: 1.25;
        }

        .ru-distribution-mini-track {
            height: 4px;
            margin-top: auto;
            padding-top: 0;
            overflow: hidden;

            background: rgba(148, 163, 184, 0.10);
            border-radius: 999px;
        }

        .ru-distribution-mini-fill {
            height: 100%;
            background: var(--ru-item-color);
            border-radius: inherit;
        }

        .ru-empty-state {
            display: flex;
            align-items: center;
            justify-content: center;

            min-height: 92px;
            padding: 1rem;

            color: #8291A5;
            background: rgba(5, 13, 24, 0.46);
            border: 1px dashed rgba(148, 163, 184, 0.17);
            border-radius: 9px;

            font-size: 0.72rem;
            line-height: 1.45;
            text-align: center;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.ru-panel-marker)
        [data-testid="stDataFrame"],
        [data-testid="stVerticalBlockBorderWrapper"]:has(.ru-panel-marker)
        [data-testid="stDataEditor"] {
            overflow: hidden;
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 10px;
        }

        @media (max-width: 1000px) {
            .ru-metric-grid--4,
            .ru-distribution-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 900px) {
            [data-testid="stMainBlockContainer"]:has(.ru-page-marker) {
                padding-right: 1rem !important;
                padding-left: 1rem !important;
            }

            .ru-dashboard-title {
                font-size: 1.65rem;
            }
        }

        @media (max-width: 640px) {
            .ru-metric-grid--2,
            .ru-metric-grid--3,
            .ru-metric-grid--4,
            .ru-distribution-grid {
                grid-template-columns: 1fr;
            }

            .ru-section-header {
                flex-direction: column;
            }

            .ru-section-meta {
                align-self: flex-start;
            }
        }
        </style>
        """
    )