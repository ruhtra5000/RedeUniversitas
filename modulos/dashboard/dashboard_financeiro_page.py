from __future__ import annotations
from typing import Any
import altair as alt
import pandas as pd
import streamlit as st
from modulos.dashboard import dashboard_service
from modulos.utils.dashboard_visual import (MetricaDashboard, criarSecaoDashboard, formatarInteiro, formatarPercentual, paraNumero, renderizarCabecalhoDashboard, renderizarMetricasDashboard)

# Cores
COR_RECEITA = "#54b68a"
COR_RECEBER = "#6f8fd3"
COR_INADIMPLENCIA = "#cf6871"
COR_BOLSA = "#8d7fd1"
COR_VENCIDA = "#d4a84f"
COR_NEUTRA = "#54a3c7"

# Função para formatar valores monetários em reais (R$) com duas casas decimais e separadores de milhar.
def formatarMoeda(valor: Any) -> str:
    numero = paraNumero(valor)

    texto = f"{numero:,.2f}"
    texto = (
        texto
        .replace(",", "_")
        .replace(".", ",")
        .replace("_", ".")
    )

    return f"R$ {texto}"

# Função para carregar o total a receber, com suporte para diferentes nomes de função no serviço de dashboard.
def carregarTotalAReceber() -> float:
    funcao = getattr(
        dashboard_service,
        "cacularTotalAReceberGeral",
        None,
    )

    if not callable(funcao):
        funcao = getattr(
            dashboard_service,
            "calcularTotalAReceberGeral",
            None,
        )

    if not callable(funcao):
        raise AttributeError(
            "Função para calcular o total a receber não encontrada "
            "no dashboard_service."
        )

    return paraNumero(funcao())

@st.cache_data(ttl=60, show_spinner=False)
# Função para carregar os indicadores financeiros, retornando um dicionário com os valores formatados.
def carregarIndicadoresFinanceiros() -> dict[str, float]:
    return {
        "receita": paraNumero(
            dashboard_service.calcularReceitaTotal()
        ),

        "a_receber": carregarTotalAReceber(),

        "inadimplentes": paraNumero(
            dashboard_service.alunosInadimplentesTotal()
        ),

        "taxa_inadimplencia": paraNumero(
            dashboard_service.taxaInadimplenciaGeral()
        ),

        "valor_inadimplente": paraNumero(
            dashboard_service.valorTotalInadimplente()
        ),

        "mensalidades_vencidas": paraNumero(
            dashboard_service.mensalidadesVencidasTotal()
        ),

        "divida_media": paraNumero(
            dashboard_service.dividaMediaTotal()
        ),

        "bolsistas": paraNumero(
            dashboard_service.alunosBolsistasTotal()
        ),

        "taxa_bolsistas": (
            paraNumero(
                dashboard_service.taxaBolsistaGeral()
            )
            * 100
        ),

        "valor_bolsas": paraNumero(
            dashboard_service.valorConcedidoPorBolsaTotal()
        ),

        "ativos": paraNumero(
            dashboard_service.alunosAtivosTotal()
        ),
    }

# Função para renderizar um rótulo de gráfico com estilo personalizado.
def rotuloGrafico(texto: str) -> None:
    st.html(
        f"""
        <div style="
            color:#8190A4;
            font-size:0.62rem;
            font-weight:800;
            letter-spacing:0.08em;
            text-transform:uppercase;
            margin-bottom:-0.25rem;
        ">
            {texto}
        </div>
        """
    )

# Função para renderizar um gráfico de valores financeiros, com barras representando receita, total a receber e valor inadimplente.
def renderizarGraficoValoresFinanceiros(*, receita: float, a_receber: float, valor_inadimplente: float) -> None:
    from modulos.utils.dashboard_graficos import renderizarGraficoBarras

    dados = pd.DataFrame(
        {
            "Indicador": [
                "Receita recebida",
                "Total a receber",
                "Valor inadimplente",
            ],

            "Valor": [
                max(receita, 0),
                max(a_receber, 0),
                max(valor_inadimplente, 0),
            ],
        }
    )

    dados["Valor formatado"] = (
        dados["Valor"]
        .apply(formatarMoeda)
    )

    ordem = [
        "Receita recebida",
        "Total a receber",
        "Valor inadimplente",
    ]

    limite = (
        None
        if float(dados["Valor"].max()) > 0
        else 1
    )

    renderizarGraficoBarras(
        dados,
        categoria="Indicador",
        valor="Valor",
        titulo="Comparativo de valores",
        ordem=ordem,
        cores={
            "Receita recebida": COR_RECEITA,
            "Total a receber": COR_RECEBER,
            "Valor inadimplente": COR_INADIMPLENCIA,
        },
        limite=limite,
        tooltip=[
            alt.Tooltip(
                "Indicador:N",
                title="Indicador",
            ),
            alt.Tooltip(
                "Valor formatado:N",
                title="Valor",
            ),
        ],
    )

# Função para renderizar um gráfico de inadimplência, mostrando a distribuição entre alunos inadimplentes e sem pendência.
def renderizarGraficoInadimplencia(*, ativos: int, inadimplentes: int) -> None:
    from modulos.utils.dashboard_graficos import renderizarGraficoBarras

    total_base = max(
        ativos,
        inadimplentes,
        0,
    )

    inadimplentes_validos = min(
        max(inadimplentes, 0),
        total_base,
    )

    sem_pendencia = max(
        total_base - inadimplentes_validos,
        0,
    )

    dados = pd.DataFrame(
        {
            "Situação": [
                "Inadimplentes",
                "Sem pendência",
            ],

            "Alunos": [
                inadimplentes_validos,
                sem_pendencia,
            ],
        }
    )

    ordem = [
        "Inadimplentes",
        "Sem pendência",
    ]

    limite = (
        None
        if int(dados["Alunos"].max()) > 0
        else 1
    )

    renderizarGraficoBarras(
        dados,
        categoria="Situação",
        valor="Alunos",
        titulo="Distribuição da inadimplência",
        ordem=ordem,
        cores={
            "Inadimplentes": COR_INADIMPLENCIA,
            "Sem pendência": COR_RECEITA,
        },
        inteiro=True,
        limite=limite,
        tooltip=[
            alt.Tooltip(
                "Situação:N",
                title="Situação",
            ),
            alt.Tooltip(
                "Alunos:Q",
                title="Alunos",
            ),
        ],
    )

# Função para renderizar um gráfico de bolsas, mostrando a distribuição entre alunos com bolsa ativa e sem bolsa ativa.
def renderizarGraficoBolsas(*, ativos: int, bolsistas: int,) -> None:
    from modulos.utils.dashboard_graficos import renderizarGraficoBarras

    total_base = max(
        ativos,
        bolsistas,
        0,
    )

    bolsistas_validos = min(
        max(bolsistas, 0),
        total_base,
    )

    sem_bolsa = max(
        total_base - bolsistas_validos,
        0,
    )

    dados = pd.DataFrame(
        {
            "Situação": [
                "Com bolsa ativa",
                "Sem bolsa ativa",
            ],

            "Alunos": [
                bolsistas_validos,
                sem_bolsa,
            ],
        }
    )

    ordem = [
        "Com bolsa ativa",
        "Sem bolsa ativa",
    ]

    limite = (
        None
        if int(dados["Alunos"].max()) > 0
        else 1
    )

    renderizarGraficoBarras(
        dados,
        categoria="Situação",
        valor="Alunos",
        titulo="Distribuição de bolsas",
        ordem=ordem,
        cores={
            "Com bolsa ativa": COR_BOLSA,
            "Sem bolsa ativa": COR_NEUTRA,
        },
        inteiro=True,
        limite=limite,
        tooltip=[
            alt.Tooltip(
                "Situação:N",
                title="Situação",
            ),
            alt.Tooltip(
                "Alunos:Q",
                title="Alunos",
            ),
        ],
    )

# Função principal para renderizar a tela do dashboard financeiro, incluindo indicadores, gráficos e seções.
def telaDashboardFinanceiro():

    atualizar = renderizarCabecalhoDashboard(
        titulo="Financeiro",
        descricao=(
            "Visão geral das receitas, inadimplências e bolsas "
            "da Rede Universitas."
        ),
        prefixo_chave="dashboard_financeiro",
    )

    if atualizar:
        carregarIndicadoresFinanceiros.clear()

    try:
        with st.spinner(
            "Carregando indicadores..."
        ):
            dados = (
                carregarIndicadoresFinanceiros()
            )

    except Exception as erro:
        st.error(
            "Não foi possível carregar os indicadores financeiros."
        )

        st.caption(
            f"Detalhes técnicos: {erro}"
        )

        return
    
    # Dados
    receita = dados[
        "receita"
    ]

    a_receber = dados[
        "a_receber"
    ]

    inadimplentes = int(
        dados["inadimplentes"]
    )

    taxa_inadimplencia = dados[
        "taxa_inadimplencia"
    ]

    valor_inadimplente = dados[
        "valor_inadimplente"
    ]

    mensalidades_vencidas = int(
        dados["mensalidades_vencidas"]
    )

    divida_media = dados[
        "divida_media"
    ]

    bolsistas = int(
        dados["bolsistas"]
    )

    taxa_bolsistas = dados[
        "taxa_bolsistas"
    ]

    valor_bolsas = dados[
        "valor_bolsas"
    ]

    ativos = int(
        dados["ativos"]
    )

    ativos_sem_bolsa = max(
        ativos - bolsistas,
        0,
    )

    receita_por_aluno = (
        receita / ativos
        if ativos
        else 0
    )

    renderizarMetricasDashboard(
        [
            MetricaDashboard(
                "Receita recebida",
                formatarMoeda(
                    receita
                ),
                "Valor efetivamente recebido pela rede.",
                COR_RECEITA,
                "RR",
            ),

            MetricaDashboard(
                "A receber",
                formatarMoeda(
                    a_receber
                ),
                "Valor que ainda deve ser recebido.",
                COR_RECEBER,
                "AR",
            ),

            MetricaDashboard(
                "Valor inadimplente",
                formatarMoeda(
                    valor_inadimplente
                ),
                (
                    "Total monetário atualmente "
                    "em inadimplência."
                ),
                COR_INADIMPLENCIA,
                "VI",
            ),

            MetricaDashboard(
                "Receita por aluno",
                formatarMoeda(
                    receita_por_aluno
                ),
                (
                    "Valor médio recebido "
                    "por aluno ativo."
                ),
                COR_NEUTRA,
                "RA",
            ),
        ],
        colunas=4,
    )

    secao_panorama = criarSecaoDashboard(
        titulo="Panorama financeiro",

        descricao=(
            "Comparativo dos principais valores movimentados "
            "e comprometidos pela rede."
        ),

        meta="Rede Universitas",

        contexto="RECEITAS E PENDÊNCIAS",

        numero=1,
    )

    with secao_panorama:

        renderizarGraficoValoresFinanceiros(
            receita=receita,
            a_receber=a_receber,
            valor_inadimplente=valor_inadimplente,
        )

    secao_inadimplencia = criarSecaoDashboard(
        titulo="Acompanhamento de inadimplências",

        descricao=(
            "Indicadores relacionados a mensalidades "
            "com pagamentos em atraso."
        ),

        meta=(
            f"{formatarInteiro(inadimplentes)} "
            f"{'aluno' if inadimplentes == 1 else 'alunos'}"
        ),

        contexto="COBRANÇAs",

        numero=2,
    )

    with secao_inadimplencia:

        renderizarMetricasDashboard(
            [
                MetricaDashboard(
                    "Alunos inadimplentes",
                    formatarInteiro(
                        inadimplentes
                    ),
                    (
                        "Alunos com pendências "
                        "financeiras."
                    ),
                    COR_INADIMPLENCIA,
                    "AI",
                ),

                MetricaDashboard(
                    "Mensalidades vencidas",
                    formatarInteiro(
                        mensalidades_vencidas
                    ),
                    (
                        "Parcelas vencidas ainda "
                        "não quitadas."
                    ),
                    COR_VENCIDA,
                    "MV",
                ),

                MetricaDashboard(
                    "Dívida média",
                    formatarMoeda(
                        divida_media
                    ),
                    (
                        "Valor médio da dívida por "
                        "aluno inadimplente."
                    ),
                    "#b383d9",
                    "DM",
                ),

                MetricaDashboard(
                    "Taxa de inadimplência",
                    formatarPercentual(
                        taxa_inadimplencia
                    ),
                    (
                        "Taxa de inadimplência "
                        "na base de alunos."
                    ),
                    COR_INADIMPLENCIA,
                    "TI",
                ),
            ],
            colunas=4,
        )


        renderizarGraficoInadimplencia(
            ativos=ativos,
            inadimplentes=inadimplentes,
        )

    secao_bolsas = criarSecaoDashboard(
        titulo="Bolsas e benefícios",

        descricao=(
            "Participação dos alunos bolsistas e impacto "
            "financeiro das bolsas ativas."
        ),

        meta=(
            f"{formatarInteiro(bolsistas)} "
            f"{'bolsista' if bolsistas == 1 else 'bolsistas'}"
        ),

        contexto="BENEFÍCIOS",

        numero=3,
    )

    with secao_bolsas:

        renderizarMetricasDashboard(
            [
                MetricaDashboard(
                    "Bolsistas ativos",
                    formatarInteiro(
                        bolsistas
                    ),
                    (
                        "Alunos atualmente vinculados "
                        "a uma bolsa ativa."
                    ),
                    COR_BOLSA,
                    "BA",
                ),

                MetricaDashboard(
                    "Taxa de bolsistas",
                    formatarPercentual(
                        taxa_bolsistas
                    ),
                    (
                        "Percentual de bolsistas "
                        "entre os alunos ativos."
                    ),
                    "#6f8fd3",
                    "TB",
                ),

                MetricaDashboard(
                    "Ativos sem bolsa",
                    formatarInteiro(
                        ativos_sem_bolsa
                    ),
                    (
                        "Alunos ativos sem "
                        "bolsa vigente."
                    ),
                    COR_NEUTRA,
                    "SB",
                ),

                MetricaDashboard(
                    "Valor concedido",
                    formatarMoeda(
                        valor_bolsas
                    ),
                    (
                        "Impacto monetário total "
                        "das bolsas concedidas."
                    ),
                    COR_BOLSA,
                    "VC",
                ),
            ],
            colunas=4,
        )

        renderizarGraficoBolsas(
            ativos=ativos,
            bolsistas=bolsistas,
        )