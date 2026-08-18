from __future__ import annotations
import unicodedata
from importlib import import_module
from typing import Any
import altair as alt
import pandas as pd
import streamlit as st
from modulos.dashboard import dashboard_service
from modulos.utils.dashboard_visual import (ItemDistribuicao, MetricaDashboard, criarSecaoDashboard, formatarInteiro, formatarPercentual, paraNumero, renderizarCabecalhoDashboard, renderizarDistribuicaoStatus, renderizarMetricasDashboard)

def obterCampusIdUsuario():
    pessoa_id = st.session_state.get("pessoa_id")
    roles = st.session_state.get("roles", [])
    
    if not pessoa_id:
        return None
        
    from database.Conexao import SessionLocal
    from sqlalchemy import select
    
    with SessionLocal() as session:
        if "REITOR" in roles:
            from database.entidades.Campus import Campus
            campus = session.execute(select(Campus).where(Campus.reitor_id == pessoa_id)).scalar_one_or_none()
            if campus: return campus.id
            
        if "ADMIN" in roles:
            return None
            
        if "ALMOXARIFE" in roles:
            from database.entidades.Almoxarife import Almoxarife
            almox = session.execute(select(Almoxarife).where(Almoxarife.pessoa_id == pessoa_id)).scalar_one_or_none()
            if almox: return almox.campus_id
            
        if "FINANCEIRO" in roles:
            from database.entidades.Financeiro import Financeiro
            fin = session.execute(select(Financeiro).where(Financeiro.pessoa_id == pessoa_id)).scalar_one_or_none()
            if fin: return fin.campus_id
            
    return None

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
def contarTrancados(campus_id: int | None = None) -> tuple[float, str | None]:
    if campus_id is None:
        contar = getattr(dashboard_service, "alunosTrancadosTotal", None)
    else:
        contar = getattr(dashboard_service, "alunosTrancadosPorCampus", None)

    if callable(contar):
        return paraNumero(contar() if campus_id is None else contar(campus_id)), None

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
def carregarIndicadoresGerais(campus_id: int | None = None) -> dict[str, Any]:
    trancados, aviso_trancados = contarTrancados(campus_id)

    if campus_id is None:
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
    else:
        return {
            "ativos": paraNumero(dashboard_service.alunosAtivosPorCampus(campus_id)),
            "trancados": trancados,
            "formados": paraNumero(dashboard_service.alunosFormadosPorCampus(campus_id)),
            "evadidos": paraNumero(dashboard_service.alunosEvadidosPorCampus(campus_id)),
            "professores": paraNumero(dashboard_service.professoresPorCampus(campus_id)),
            "cursos": paraNumero(dashboard_service.cursosPorCampus(campus_id)),
            "taxa_evasao": paraNumero(dashboard_service.taxaEvasaoPorCampus(campus_id)),
            "aviso_trancados": aviso_trancados,
        }

# Função para renderizar o gráfico de situação dos alunos, mostrando a distribuição percentual de alunos ativos, trancados, formados e evadidos.
def renderizarGraficoSituacaoAluno(status: list[ItemDistribuicao]) -> None:
    from modulos.utils.dashboard_graficos import renderizarGraficoBarras

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
    cores = {
        item.rotulo: item.cor
        for item in status
    }

    renderizarGraficoBarras(
        dados,
        categoria="Situação",
        valor="Percentual",
        titulo="Comparativo visual",
        ordem=ordem,
        cores=cores,
        limite=100,
        percentual=True,
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

# Função para renderizar o gráfico de estrutura acadêmica como donut chart, mostrando a proporção entre alunos, professores e cursos.
def renderizarGraficoEstrutura(*, total_alunos: int, professores: int, cursos: int) -> None:
    from modulos.utils.dashboard_graficos import rotuloGrafico

    total = total_alunos + professores + cursos

    if total <= 0:
        return

    dados = pd.DataFrame(
        {
            "Categoria": [
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

    dados["Percentual"] = (dados["Quantidade"] / total * 100).round(1)

    grafico = (
        alt.Chart(dados)
        .mark_arc(
            innerRadius=78,
            outerRadius=125,
            stroke=None,
        )
        .encode(
            theta=alt.Theta(
                "Quantidade:Q",
                stack=True,
            ),
            color=alt.Color(
                "Categoria:N",
                scale=alt.Scale(
                    domain=["Alunos", "Professores", "Cursos"],
                    range=["#C49A4A", "#6f8fd3", "#8d7fd1"],
                ),
                legend=alt.Legend(
                    orient="right",
                    labelColor="#8FA0B6",
                    labelFontSize=10,
                    symbolSize=90,
                    symbolType="circle",
                    title=None,
                    rowPadding=6,
                ),
            ),
            tooltip=[
                alt.Tooltip("Categoria:N", title="Categoria"),
                alt.Tooltip("Quantidade:Q", title="Quantidade", format=",d"),
                alt.Tooltip("Percentual:Q", title="Participação (%)", format=".1f"),
            ],
        )
        .properties(height=290)
        .configure_view(stroke=None)
        .configure(background="transparent")
    )

    rotuloGrafico("Composição estrutural")
    st.altair_chart(grafico, use_container_width=True, theme=None)

# Função principal para renderizar a tela do dashboard geral, exibindo indicadores de alunos, professores e cursos, bem como gráficos de situação e estrutura acadêmica.
def telaDashboardGeral():
    campus_id = obterCampusIdUsuario()
    campus_nome = None
    
    if campus_id is not None:
        from database.Conexao import SessionLocal
        from sqlalchemy import select
        from database.entidades.Campus import Campus
        with SessionLocal() as session:
            campus_obj = session.execute(select(Campus).where(Campus.id == campus_id)).scalar_one_or_none()
            if campus_obj:
                campus_nome = campus_obj.nome
    
    atualizar = renderizarCabecalhoDashboard(
        titulo="Geral" if campus_nome is None else f"Geral",
        descricao=(
            "Resumo dos vínculos acadêmicos e da estrutura atual da Rede Universitas." if campus_nome is None else
            f"Resumo dos vínculos acadêmicos e da estrutura atual ({campus_nome})."
        ),
        prefixo_chave="dashboard_geral",
    )

    if atualizar:
        carregarIndicadoresGerais.clear()

    try:
        with st.spinner("Carregando indicadores..."):
            dados = carregarIndicadoresGerais(campus_id)
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
        col_cards, col_grafico = st.columns(
            [1, 1],
            gap="large",
            vertical_alignment="center",
        )

        with col_cards:
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
                colunas=2,
            )

        with col_grafico:
            renderizarGraficoEstrutura(
                total_alunos=total_alunos,
                professores=professores,
                cursos=cursos,
            )

    if dados["aviso_trancados"]:
        st.caption(dados["aviso_trancados"])