from __future__ import annotations
import unicodedata
from importlib import import_module
from typing import Any
import altair as alt
import pandas as pd
import streamlit as st
from modulos.dashboard import dashboard_service
from modulos.utils.dashboard_visual import (ItemDistribuicao, MetricaDashboard, criarSecaoDashboard, formatarInteiro, formatarPercentual, paraNumero, renderizarCabecalhoDashboard, renderizarDistribuicaoStatus, renderizarMetricasDashboard)

# Cores
COR_ATIVO = "#54b68a"
COR_TRANCADO = "#d4a84f"
COR_FORMADO = "#6f8fd3"
COR_EVADIDO = "#cf6871"

# Função para normalizar texto, removendo acentos e convertendo para maiúsculas
def normalizarTexto(valor: Any) -> str:
    texto = unicodedata.normalize("NFKD", str(valor or ""))
    texto = "".join(
        caractere
        for caractere in texto
        if not unicodedata.combining(caractere)
    )
    return texto.strip().upper()

# Função para obter o status do aluno, considerando diferentes tipos de entrada (dicionário, objeto com mapeamento ou objeto com atributos)
def obterStatusAluno(aluno: Any) -> str:
    if isinstance(aluno, dict):
        status = aluno.get("status") or aluno.get("situacao")
    elif hasattr(aluno, "_mapping"):
        mapeamento = aluno._mapping
        status = mapeamento.get("status") or mapeamento.get("situacao")
    else:
        status = getattr(aluno, "status", None)
        if status is None:
            status = getattr(aluno, "situacao", None)

    if hasattr(status, "name"):
        status = status.name
    elif hasattr(status, "value"):
        status = status.value

    return normalizarTexto(status)

# Função para contar o número de alunos com curso trancado.
def contarTrancados() -> tuple[float, str | None]:
    contar = getattr(dashboard_service, "alunosTrancadosTotal", None)

    if callable(contar):
        return paraNumero(contar()), None

    try:
        academico_service = import_module(
            "modulos.academico.academico_service"
        )

        listar = None
        for nome_funcao in ("listarAlunosGeral", "listarAlunos"):
            candidata = getattr(academico_service, nome_funcao, None)
            if callable(candidata):
                listar = candidata
                break

        if listar is None:
            raise AttributeError("função de listagem geral não encontrada")

        alunos = listar() or []
        quantidade = sum(
            1
            for aluno in alunos
            if "TRANCAD" in obterStatusAluno(aluno)
        )
        return float(quantidade), None

    except Exception:
        return 0.0, (
            "Adicione alunosTrancadosTotal() ao dashboard_service para obter "
            "a contagem de alunos com curso trancado."
        )

@st.cache_data(ttl=60, show_spinner=False)
# Função para carregar os indicadores gerais do dashboard, incluindo ativos, trancados, formados, evadidos, professores, cursos e taxa de evasão.
def carregarIndicadoresGerais() -> dict[str, Any]:
    trancados, aviso_trancados = contarTrancados()

    return {
        "ativos": paraNumero(dashboard_service.alunosAtivosTotal()),
        "trancados": trancados,
        "formados": paraNumero(dashboard_service.alunosFormadosTotal()),
        "evadidos": paraNumero(dashboard_service.alunosEvadidosTotal()),
        "professores": paraNumero(dashboard_service.professoresTotal()),
        "cursos": paraNumero(dashboard_service.cursosTotal()),
        "taxa_evasao": paraNumero(dashboard_service.taxaEvasaoGeral()),
        "aviso_trancados": aviso_trancados,
    }

# Função para renderizar o gráfico de situação dos alunos, mostrando a distribuição percentual de alunos ativos, trancados, formados e evadidos.
def renderizarGraficoSituacaoAluno(status: list[ItemDistribuicao]) -> None:
    total = sum(max(item.valor, 0) for item in status)

    if total <= 0:
        return

    dados = pd.DataFrame(
        [
            {
                "Situação": item.rotulo,
                "Alunos": max(item.valor, 0),
                "Percentual": (
                    max(item.valor, 0) / total
                ) * 100,
            }
            for item in status
        ]
    )

    ordem = [item.rotulo for item in status]

    grafico = (
        alt.Chart(dados)
        .mark_bar(
            cornerRadiusTopRight=5,
            cornerRadiusBottomRight=5,
            size=18,
        )
        .encode(
            y=alt.Y(
                "Situação:N",
                sort=ordem,
                title=None,
                axis=alt.Axis(
                    labelColor="#8FA0B6",
                    labelFontSize=11,
                    labelPadding=10,
                    ticks=False,
                    domain=False,
                ),
            ),
            x=alt.X(
                "Percentual:Q",
                title=None,
                scale=alt.Scale(domain=[0, 100]),
                axis=alt.Axis(
                    labelColor="#66778D",
                    labelFontSize=10,
                    labelExpr="datum.value + '%'",
                    grid=True,
                    gridColor="rgba(148,163,184,0.08)",
                    ticks=False,
                    domain=False,
                ),
            ),
            color=alt.Color(
                "Situação:N",
                scale=alt.Scale(
                    domain=[
                        "Ativos",
                        "Trancados",
                        "Formados",
                        "Evadidos",
                    ],
                    range=[
                        "#54b68a",
                        "#d4a84f",
                        "#6f8fd3",
                        "#cf6871",
                    ],
                ),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("Situação:N", title="Situação"),
                alt.Tooltip("Alunos:Q", title="Alunos"),
                alt.Tooltip(
                    "Percentual:Q",
                    title="Participação",
                    format=".1f",
                ),
            ],
        )
        .properties(height=165)
        .configure_view(stroke=None)
        .configure(background="transparent")
    )

    st.html(
        """
        <div style="
            color:#8190A4;
            font-size:0.62rem;
            font-weight:800;
            letter-spacing:0.08em;
            text-transform:uppercase;
            margin-bottom:-0.25rem;
        ">
            Comparativo visual
        </div>
        """
    )

    st.altair_chart(
        grafico,
        use_container_width=True,
        theme=None,
    )

# Função para renderizar o gráfico de estrutura acadêmica, mostrando a quantidade de alunos, professores e cursos na rede.
def renderizarGraficoEstrutura(*, total_alunos: int, professores: int, cursos: int) -> None:
    dados = pd.DataFrame(
        {
            "Indicador": [
                "Alunos",
                "Professores",
                "Cursos",
            ],
            "Quantidade": [
                total_alunos,
                professores,
                cursos,
            ],
        }
    )

    if int(dados["Quantidade"].sum()) <= 0:
        return

    grafico = (
        alt.Chart(dados)
        .mark_bar(
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5,
            size=44,
        )
        .encode(
            x=alt.X(
                "Indicador:N",
                sort=None,
                title=None,
                axis=alt.Axis(
                    labelColor="#8FA0B6",
                    labelFontSize=10,
                    labelAngle=0,
                    labelPadding=10,
                    ticks=False,
                    domain=False,
                ),
            ),
            y=alt.Y(
                "Quantidade:Q",
                title=None,
                axis=alt.Axis(
                    labelColor="#66778D",
                    labelFontSize=10,
                    tickMinStep=1,
                    grid=True,
                    gridColor="rgba(148,163,184,0.08)",
                    ticks=False,
                    domain=False,
                ),
            ),
            color=alt.Color(
                "Indicador:N",
                scale=alt.Scale(
                    domain=[
                        "Alunos",
                        "Professores",
                        "Cursos",
                    ],
                    range=[
                        "#C49A4A",
                        "#6f8fd3",
                        "#8d7fd1",
                    ],
                ),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("Indicador:N", title="Indicador"),
                alt.Tooltip("Quantidade:Q", title="Quantidade"),
            ],
        )
        .properties(height=175)
        .configure_view(stroke=None)
        .configure(background="transparent")
    )

    st.html(
        """
        <div style="
            color:#8190A4;
            font-size:0.62rem;
            font-weight:800;
            letter-spacing:0.08em;
            text-transform:uppercase;
            margin-bottom:-0.25rem;
        ">
            Estrutura em números
        </div>
        """
    )

    st.altair_chart(
        grafico,
        use_container_width=True,
        theme=None,
    )

# Função principal para renderizar a tela do dashboard geral, exibindo indicadores de alunos, professores e cursos, bem como gráficos de situação e estrutura acadêmica.
def telaDashboardGeral():
    atualizar = renderizarCabecalhoDashboard(
        titulo="Geral",
        descricao=(
            "Resumo dos vínculos acadêmicos e da estrutura atual da Rede Universitas."
        ),
        prefixo_chave="dashboard_geral",
    )

    if atualizar:
        carregarIndicadoresGerais.clear()

    try:
        with st.spinner("Carregando indicadores..."):
            dados = carregarIndicadoresGerais()
    except Exception as erro:
        st.error("Não foi possível carregar os indicadores gerais.")
        st.caption(f"Detalhes técnicos: {erro}")
        return

    ativos = int(dados["ativos"])
    trancados = int(dados["trancados"])
    formados = int(dados["formados"])
    evadidos = int(dados["evadidos"])
    professores = int(dados["professores"])
    cursos = int(dados["cursos"])

    status = [
        ItemDistribuicao("Ativos", ativos, COR_ATIVO),
        ItemDistribuicao("Trancados", trancados, COR_TRANCADO),
        ItemDistribuicao("Formados", formados, COR_FORMADO),
        ItemDistribuicao("Evadidos", evadidos, COR_EVADIDO),
    ]

    total_alunos = sum(item.valor for item in status)

    percentual_ativos = (
        (ativos / total_alunos) * 100 if total_alunos else 0
    )
    percentual_trancados = (
        (trancados / total_alunos) * 100 if total_alunos else 0
    )

    alunos_por_professor = (
        total_alunos / professores if professores else None
    )
    alunos_por_curso = (
        total_alunos / cursos if cursos else None
    )

    renderizarMetricasDashboard(
        [
            MetricaDashboard(
                "Total de alunos",
                formatarInteiro(total_alunos),
                "Todos os vínculos acadêmicos cadastrados na rede"
                "TA",
            ),
            MetricaDashboard(
                "Ativos",
                formatarInteiro(ativos),
                f"{formatarPercentual(percentual_ativos)} do corpo discente.",
                COR_ATIVO,
                "AT",
            ),
            MetricaDashboard(
                "Trancados",
                formatarInteiro(trancados),
                f"{formatarPercentual(percentual_trancados)} dos vínculos.",
                COR_TRANCADO,
                "TR",
            ),
            MetricaDashboard(
                "Taxa de evasão",
                formatarPercentual(dados["taxa_evasao"]),
                (
                    f"{formatarInteiro(evadidos)} "
                    f"{'aluno evadido' if evadidos == 1 else 'alunos evadidos'}."
                ),
                COR_EVADIDO,
                "TE",
            ),
        ],
        colunas=4,
    )

    secao_status = criarSecaoDashboard(
        titulo="Situação do corpo discente",
        descricao=(
            "Distribuição dos alunos conforme o status atual do vínculo "
            "acadêmico."
        ),
        meta=f"{formatarInteiro(total_alunos)} alunos",
        contexto="CORPO DISCENTE",
        numero=1,
    )

    with secao_status:
        renderizarDistribuicaoStatus(status)

        renderizarGraficoSituacaoAluno(
            status
        )

    secao_estrutura = criarSecaoDashboard(
        titulo="Estrutura acadêmica",
        descricao=(
            "Capacidade atual da rede e da relação entre alunos, "
            "docentes e cursos."
        ),
        meta="Rede Universitas",
        contexto="ESTRUTURA",
        numero=2,
    )

    with secao_estrutura:
        renderizarMetricasDashboard(
            [
                MetricaDashboard(
                    "Professores",
                    formatarInteiro(professores),
                    "Docentes atualmente vinculados à rede.",
                    "#6f8fd3",
                    "PR",
                ),
                MetricaDashboard(
                    "Cursos",
                    formatarInteiro(cursos),
                    "Cursos cadastrados e disponíveis na rede.",
                    "#8d7fd1",
                    "CU",
                ),
                MetricaDashboard(
                    "Alunos por professor",
                    (
                        f"{alunos_por_professor:.1f}".replace(".", ",")
                        if alunos_por_professor is not None
                        else "—"
                    ),
                    "Relação média entre vínculos envolvendo discentes e docentes.",
                    "#54a3c7",
                    "AP",
                ),
                MetricaDashboard(
                    "Alunos por curso",
                    (
                        f"{alunos_por_curso:.1f}".replace(".", ",")
                        if alunos_por_curso is not None
                        else "—"
                    ),
                    "Quantidade média de alunos por curso cadastrado.",
                    "#b383d9",
                    "AC",
                ),
            ],
            colunas=4,
        )

        renderizarGraficoEstrutura(
            total_alunos=total_alunos,
            professores=professores,
            cursos=cursos,
        )

    if dados["aviso_trancados"]:
        st.caption(dados["aviso_trancados"])