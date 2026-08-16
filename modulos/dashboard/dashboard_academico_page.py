from __future__ import annotations
import unicodedata
from collections.abc import Mapping
from typing import Any
import altair as alt
import pandas as pd
import streamlit as st
from modulos.dashboard import dashboard_service
from modulos.utils.dashboard_visual import (ItemDistribuicao, MetricaDashboard, criarSecaoDashboard, formatarDecimal, formatarInteiro, formatarPercentual, paraNumero, renderizarCabecalhoDashboard, renderizarEstadoVazio, renderizarDistribuicaoStatus, renderizarMetricasDashboard)

# CORES E ORDEM
ORDEM_DESEMPENHO = ["Excelente", "Bom", "Regular", "Ruim"]
CORES_DESEMPENHO = {
    "Excelente": "#6f8fd3",
    "Bom": "#54b68a",
    "Regular": "#d4a84f",
    "Ruim": "#cf6871",
}

# Função para normalizar chaves de mapeamento, removendo acentos, espaços e convertendo para minúsculas.
def normalizarChave(valor: Any) -> str:
    texto = unicodedata.normalize("NFKD", str(valor))
    texto = "".join(caractere for caractere in texto if not unicodedata.combining(caractere))
    return texto.strip().lower().replace(" ", "_")

# Função para mapear valores de desempenho para categorias padronizadas.
def categoriaDesempenho(valor: Any) -> str | None:
    categorias = {
        "excelente": "Excelente",
        "bom": "Bom",
        "regular": "Regular",
        "ruim": "Ruim",
    }
    return categorias.get(normalizarChave(valor))

# Função para converter um registro em um dicionário, lidando com diferentes tipos de entrada.
def comoMapeamento(registro: Any) -> dict[str, Any]:
    if isinstance(registro, Mapping):
        return dict(registro)

    if hasattr(registro, "_mapping"):
        return dict(registro._mapping)

    return {}

# Função para obter o primeiro valor correspondente a uma lista de nomes possíveis em um mapeamento.
def primeiroValor(mapeamento: Mapping[str, Any], nomes: tuple[str, ...]) -> Any:
    valores_normalizados = {
        normalizarChave(chave): valor for chave, valor in mapeamento.items()
    }

    for nome in nomes:
        chave = normalizarChave(nome)
        if chave in valores_normalizados:
            return valores_normalizados[chave]

    return None

# Função para normalizar os dados de desempenho, garantindo que todas as categorias estejam presentes e com valores numéricos.
def normalizarDesempenho(dados: Any) -> pd.DataFrame:
    quantidades = {categoria: 0 for categoria in ORDEM_DESEMPENHO}

    if dados is None:
        dados = []

    if isinstance(dados, pd.DataFrame):
        registros = dados.to_dict("records")
    elif isinstance(dados, Mapping):
        categorias_nas_chaves = [
            (categoriaDesempenho(chave), valor) for chave, valor in dados.items()
        ]

        if any(categoria is not None for categoria, _ in categorias_nas_chaves):
            for categoria, quantidade in categorias_nas_chaves:
                if categoria is not None:
                    quantidades[categoria] = int(round(paraNumero(quantidade)))

            return pd.DataFrame(
                {
                    "Categoria": ORDEM_DESEMPENHO,
                    "Quantidade": [
                        quantidades[categoria] for categoria in ORDEM_DESEMPENHO
                    ],
                }
            )

        registros = [dados]
    elif (
        isinstance(dados, tuple)
        and len(dados) >= 2
        and categoriaDesempenho(dados[0]) is not None
    ):
        registros = [dados]
    else:
        registros = list(dados) if isinstance(dados, (list, tuple)) else [dados]

    for registro in registros:
        mapeamento = comoMapeamento(registro)

        if mapeamento:
            categoria = primeiroValor(
                mapeamento,
                ("categoria", "desempenho", "classificacao", "faixa"),
            )
            quantidade = primeiroValor(
                mapeamento,
                ("quantidade", "total", "qtd", "count", "contagem"),
            )
        elif isinstance(registro, (list, tuple)) and len(registro) >= 2:
            categoria, quantidade = registro[0], registro[1]
        else:
            categoria = getattr(registro, "categoria", None)
            quantidade = getattr(registro, "quantidade", None)

        categoria_normalizada = categoriaDesempenho(categoria)
        if categoria_normalizada is not None:
            quantidades[categoria_normalizada] = int(
                round(paraNumero(quantidade))
            )

    return pd.DataFrame(
        {
            "Categoria": ORDEM_DESEMPENHO,
            "Quantidade": [quantidades[categoria] for categoria in ORDEM_DESEMPENHO],
        }
    )

# Função para acessar atributos de um objeto de forma segura, retornando None em caso de erro.
def atributoSeguro(objeto: Any, nome: str) -> Any:
    try:
        return getattr(objeto, nome, None)
    except Exception:
        return None

# Função para acrescentar informações de um objeto a um mapeamento, lidando com diferentes tipos de atributos e nomes de classes.
def acrescentarObjeto(mapeamento: dict[str, Any], objeto: Any) -> None:
    if objeto is None or isinstance(objeto, (str, int, float, bool)):
        return

    nome_classe = objeto.__class__.__name__.lower()

    for atributo in (
        "matricula",
        "coef_rend",
        "coeficiente_rendimento",
        "cr",
        "reprovacoes",
        "quantidade_reprovacoes",
        "total_reprovacoes",
    ):
        valor = atributoSeguro(objeto, atributo)
        if valor is not None:
            mapeamento.setdefault(atributo, valor)

    nome = atributoSeguro(objeto, "nome")
    if nome is not None:
        if "curso" in nome_classe:
            mapeamento.setdefault("curso_nome", nome)
        elif "campus" in nome_classe:
            mapeamento.setdefault("campus_nome", nome)
        elif "pessoa" in nome_classe:
            mapeamento.setdefault("aluno_nome", nome)
        else:
            mapeamento.setdefault("nome", nome)

    pessoa = atributoSeguro(objeto, "pessoa")
    if pessoa is not None:
        nome_pessoa = atributoSeguro(pessoa, "nome")
        if nome_pessoa is not None:
            mapeamento.setdefault("aluno_nome", nome_pessoa)

    curso = atributoSeguro(objeto, "curso")
    if curso is not None:
        nome_curso = atributoSeguro(curso, "nome")
        if nome_curso is not None:
            mapeamento.setdefault("curso_nome", nome_curso)

    campus = atributoSeguro(objeto, "campus")
    if campus is not None:
        nome_campus = atributoSeguro(campus, "nome")
        if nome_campus is not None:
            mapeamento.setdefault("campus_nome", nome_campus)

# Função para mapear um registro de aluno em um dicionário, lidando com diferentes tipos de entrada e extraindo informações relevantes.
def _mapearRegistroAluno(registro: Any) -> dict[str, Any]:
    mapeamento = comoMapeamento(registro)

    if not mapeamento and isinstance(registro, (list, tuple)):
        for item in registro:
            submapeamento = comoMapeamento(item)
            mapeamento.update(submapeamento)
            acrescentarObjeto(mapeamento, item)
    else:
        for item in list(mapeamento.values()):
            acrescentarObjeto(mapeamento, item)

    acrescentarObjeto(mapeamento, registro)
    return mapeamento

# Função para normalizar os dados de alunos com baixo desempenho, garantindo que todas as informações relevantes estejam presentes e em formato adequado.
def normalizarAlunosBaixoDesempenho(dados: Any) -> pd.DataFrame:
    colunas = ["Aluno", "Matrícula", "Curso", "Campus", "CR", "Reprovações"]

    if dados is None:
        return pd.DataFrame(columns=colunas)

    if isinstance(dados, pd.DataFrame):
        registros = dados.to_dict("records")
    elif isinstance(dados, Mapping):
        registros = [dados]
    elif isinstance(dados, (list, tuple)):
        registros = list(dados)
    else:
        registros = [dados]

    linhas = []

    for registro in registros:
        mapeamento = _mapearRegistroAluno(registro)

        nome = primeiroValor(
            mapeamento,
            ("aluno_nome", "nome_aluno", "nome", "pessoa_nome"),
        )
        matricula = primeiroValor(
            mapeamento,
            ("matricula", "numero_matricula"),
        )
        curso = primeiroValor(
            mapeamento,
            ("curso_nome", "nome_curso", "curso"),
        )
        campus = primeiroValor(
            mapeamento,
            ("campus_nome", "nome_campus", "campus"),
        )
        cr = primeiroValor(
            mapeamento,
            ("coef_rend", "coeficiente_rendimento", "cr", "media_geral"),
        )
        reprovacoes = primeiroValor(
            mapeamento,
            (
                "reprovacoes",
                "quantidade_reprovacoes",
                "total_reprovacoes",
                "qtd_reprovacoes",
            ),
        )

        if hasattr(curso, "nome"):
            curso = atributoSeguro(curso, "nome")
        if hasattr(campus, "nome"):
            campus = atributoSeguro(campus, "nome")

        linhas.append(
            {
                "Aluno": nome or "Não informado",
                "Matrícula": matricula or "Não informada",
                "Curso": curso or "Não informado",
                "Campus": campus or "Não informado",
                "CR": paraNumero(cr) if cr is not None else None,
                "Reprovações": int(round(paraNumero(reprovacoes))),
            }
        )

    return pd.DataFrame(linhas, columns=colunas)

@st.cache_data(ttl=60, show_spinner=False)
# Função para carregar o coeficiente de rendimento médio (CR) total, utilizando cache para otimização.
def carregarCrMedio() -> float:
    return paraNumero(dashboard_service.crMedioTotal())

@st.cache_data(ttl=60, show_spinner=False)
# Função para carregar os dados de desempenho dos alunos, utilizando cache para otimização.
def carregarDesempenho() -> pd.DataFrame:
    return normalizarDesempenho(
        dashboard_service.agruparAlunosDesempenhoGeral()
    )

@st.cache_data(ttl=60, show_spinner=False)
# Função para carregar os dados de alunos com baixo desempenho, utilizando cache para otimização.
def carregarBaixoDesempenho() -> pd.DataFrame:
    return normalizarAlunosBaixoDesempenho(
        dashboard_service.listarAlunosBaixoDesempenhoGeral()
    )

# Função para renderizar o gráfico de desempenho dos alunos, utilizando Altair para visualização.
def renderizarGraficoDesempenho(faixas: list[ItemDistribuicao]) -> None:
    total = sum(max(item.valor, 0) for item in faixas)

    if total <= 0:
        return

    dados = pd.DataFrame(
        [
            {
                "Faixa": item.rotulo,
                "Alunos": max(item.valor, 0),
                "Percentual": (
                    max(item.valor, 0) / total
                ) * 100,
            }
            for item in faixas
        ]
    )

    ordem = [item.rotulo for item in faixas]

    grafico = (
        alt.Chart(dados)
        .mark_bar(
            cornerRadiusTopRight=5,
            cornerRadiusBottomRight=5,
            size=18,
        )
        .encode(
            y=alt.Y(
                "Faixa:N",
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
                "Faixa:N",
                scale=alt.Scale(
                    domain=[
                        "Excelente",
                        "Bom",
                        "Regular",
                        "Ruim",
                    ],
                    range=[
                        "#6f8fd3",
                        "#54b68a",
                        "#d4a84f",
                        "#cf6871",
                    ],
                ),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("Faixa:N", title="Faixa"),
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

# Função para renderizar o gráfico de acompanhamento acadêmico, comparando os critérios de baixo desempenho dos alunos.
def renderizarGraficoAcompanhamento(*, cr_baixo: int, muitas_reprovacoes: int, ambos_criterios: int) -> None:
    dados = pd.DataFrame(
        {
            "Critério": [
                "CRM abaixo de 5,5",
                "3+ reprovações",
                "Ambos os critérios",
            ],
            "Alunos": [
                cr_baixo,
                muitas_reprovacoes,
                ambos_criterios,
            ],
        }
    )

    if int(dados["Alunos"].sum()) <= 0:
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
                "Critério:N",
                sort=None,
                title=None,
                axis=alt.Axis(
                    labelColor="#8FA0B6",
                    labelFontSize=10,
                    labelAngle=0,
                    labelLimit=160,
                    labelPadding=10,
                    ticks=False,
                    domain=False,
                ),
            ),
            y=alt.Y(
                "Alunos:Q",
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
                "Critério:N",
                scale=alt.Scale(
                    domain=[
                        "CRM abaixo de 5,5",
                        "3+ reprovações",
                        "Ambos os critérios",
                    ],
                    range=[
                        "#cf6871",
                        "#d4a84f",
                        "#8d7fd1",
                    ],
                ),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("Critério:N", title="Critério"),
                alt.Tooltip("Alunos:Q", title="Alunos"),
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
            Comparativo dos critérios
        </div>
        """
    )

    st.altair_chart(
        grafico,
        use_container_width=True,
        theme=None,
    )

# Função principal para renderizar a tela do dashboard acadêmico, incluindo métricas, gráficos e tabelas de desempenho dos alunos.
def telaDashboardAcademico():

    atualizar = renderizarCabecalhoDashboard(
        titulo="Acadêmico",
        descricao=(
            "Rendimento dos alunos e situações que exigem acompanhamento da "
            "equipe acadêmica."
        ),
        prefixo_chave="dashboard_academico",
    )

    if atualizar:
        carregarCrMedio.clear()
        carregarDesempenho.clear()
        carregarBaixoDesempenho.clear()

    cr_medio = None
    desempenho = pd.DataFrame(
        {
            "Categoria": ORDEM_DESEMPENHO,
            "Quantidade": [0, 0, 0, 0],
        }
    )
    baixo_desempenho = pd.DataFrame(
        columns=[
            "Aluno",
            "Matrícula",
            "Curso",
            "Campus",
            "CR",
            "Reprovações",
        ]
    )

    erro_cr = None
    erro_desempenho = None
    erro_baixo_desempenho = None

    with st.spinner("Carregando indicadores..."):
        try:
            cr_medio = carregarCrMedio()
        except Exception as erro:
            erro_cr = erro

        try:
            desempenho = carregarDesempenho()
        except Exception as erro:
            erro_desempenho = erro

        try:
            baixo_desempenho = carregarBaixoDesempenho()
        except Exception as erro:
            erro_baixo_desempenho = erro

    quantidades = (
        desempenho
        .set_index("Categoria")["Quantidade"]
        .to_dict()
    )

    excelentes = int(quantidades.get("Excelente", 0))
    bons = int(quantidades.get("Bom", 0))
    regulares = int(quantidades.get("Regular", 0))
    ruins = int(quantidades.get("Ruim", 0))

    total_avaliados = (
        excelentes
        + bons
        + regulares
        + ruins
    )

    alto_desempenho = excelentes + bons

    percentual_alto = (
        (alto_desempenho / total_avaliados) * 100
        if total_avaliados
        else 0
    )

    faixas_desempenho = [
        ItemDistribuicao(
            "Excelente",
            excelentes,
            CORES_DESEMPENHO["Excelente"],
        ),
        ItemDistribuicao(
            "Bom",
            bons,
            CORES_DESEMPENHO["Bom"],
        ),
        ItemDistribuicao(
            "Regular",
            regulares,
            CORES_DESEMPENHO["Regular"],
        ),
        ItemDistribuicao(
            "Ruim",
            ruins,
            CORES_DESEMPENHO["Ruim"],
        ),
    ]

    if erro_baixo_desempenho is None:
        cr_numerico = pd.to_numeric(
            baixo_desempenho["CR"],
            errors="coerce",
        )

        reprovacoes_numerico = pd.to_numeric(
            baixo_desempenho["Reprovações"],
            errors="coerce",
        ).fillna(0)

        criterio_cr = cr_numerico < 5.5
        criterio_reprovacao = reprovacoes_numerico >= 3

        alunos_cr_baixo = int(criterio_cr.sum())
        alunos_muitas_reprovacoes = int(
            criterio_reprovacao.sum()
        )
        alunos_ambos_criterios = int(
            (criterio_cr & criterio_reprovacao).sum()
        )
        total_reprovacoes_atencao = int(
            reprovacoes_numerico.sum()
        )
    else:
        alunos_cr_baixo = 0
        alunos_muitas_reprovacoes = 0
        alunos_ambos_criterios = 0
        total_reprovacoes_atencao = 0

    renderizarMetricasDashboard(
        [
            MetricaDashboard(
                "CRM médio",
                (
                    formatarDecimal(cr_medio, 2)
                    if cr_medio is not None
                    else "—"
                ),
                (
                    "Coeficiente de rendimento médio da instituição."
                    if erro_cr is None
                    else "Indicador temporariamente indisponível."
                ),
                "#6f8fd3",
                "CR",
            ),
            MetricaDashboard(
                "Alunos avaliados",
                (
                    formatarInteiro(total_avaliados)
                    if erro_desempenho is None
                    else "—"
                ),
                "Alunos distribuídos nas faixas de rendimento.",
                "#C49A4A",
                "AA",
            ),
            MetricaDashboard(
                "Bom ou excelente",
                (
                    formatarInteiro(alto_desempenho)
                    if erro_desempenho is None
                    else "—"
                ),
                (
                    f"{formatarPercentual(percentual_alto)} dos avaliados."
                    if erro_desempenho is None
                    else "Indicador temporariamente indisponível."
                ),
                "#54b68a",
                "BE",
            ),
            MetricaDashboard(
                "Baixo desempenho",
                (
                    formatarInteiro(len(baixo_desempenho))
                    if erro_baixo_desempenho is None
                    else "—"
                ),
                "CRM menor que 5,5 ou três ou mais reprovações.",
                "#cf6871",
                "BD",
            ),
        ],
        colunas=4,
    )

    secao_desempenho = criarSecaoDashboard(
        titulo="Distribuição de desempenho",
        descricao=(
            "Participação dos alunos em cada faixa de rendimento acadêmico."
        ),
        meta=(
            f"{formatarInteiro(total_avaliados)} avaliados"
            if erro_desempenho is None
            else "Indisponível"
        ),
        contexto="DESEMPENHO",
        numero=1,
    )

    with secao_desempenho:
        if erro_desempenho is not None:
            st.warning(
                "Não foi possível carregar as faixas de desempenho."
            )
        else:
            renderizarDistribuicaoStatus(
                faixas_desempenho
            )

            renderizarGraficoDesempenho(
                faixas_desempenho
            )

    secao_diagnostico = criarSecaoDashboard(
        titulo="Diagnóstico de acompanhamento",
        descricao=(
            "Detalhamento dos critérios que levaram alunos para a lista de "
            "acompanhamento acadêmico."
        ),
        meta=(
            f"{formatarInteiro(len(baixo_desempenho))} casos"
            if erro_baixo_desempenho is None
            else "Indisponível"
        ),
        contexto="ATENÇÃO ACADÊMICA",
        numero=2,
    )

    with secao_diagnostico:
        if erro_baixo_desempenho is not None:
            st.warning(
                "Não foi possível calcular os indicadores de acompanhamento."
            )
        else:
            renderizarMetricasDashboard(
                [
                    MetricaDashboard(
                        "CRM abaixo de 5,5",
                        formatarInteiro(alunos_cr_baixo),
                        (
                            "Alunos com coeficiente abaixo "
                            "do limite."
                        ),
                        "#cf6871",
                        "CR",
                    ),
                    MetricaDashboard(
                        "3+ reprovações",
                        formatarInteiro(
                            alunos_muitas_reprovacoes
                        ),
                        (
                            "Alunos com três ou mais "
                            "reprovações registradas."
                        ),
                        "#d4a84f",
                        "RP",
                    ),
                    MetricaDashboard(
                        "Ambos os critérios",
                        formatarInteiro(
                            alunos_ambos_criterios
                        ),
                        (
                            "Alunos que atendem simultaneamente "
                            "aos dois critérios."
                        ),
                        "#8d7fd1",
                        "2C",
                    ),
                    MetricaDashboard(
                        "Total de Reprovações",
                        formatarInteiro(
                            total_reprovacoes_atencao
                        ),
                        (
                            "Total de reprovações acumuladas "
                            "pelos alunos em atenção."
                        ),
                        "#6f8fd3",
                        "TR",
                    ),
                ],
                colunas=4,
            )

            renderizarGraficoAcompanhamento(
                cr_baixo=alunos_cr_baixo,
                muitas_reprovacoes=alunos_muitas_reprovacoes,
                ambos_criterios=alunos_ambos_criterios,
            )

    secao_tabela = criarSecaoDashboard(
        titulo="Alunos que precisam de acompanhamento",
        descricao=(
            "Estudantes com CRM menor que 5,5 ou com três ou mais reprovações."
        ),
        meta=(
            f"{formatarInteiro(len(baixo_desempenho))} alunos"
            if erro_baixo_desempenho is None
            else "Indisponível"
        ),
        contexto="ACOMPANHAMENTO",
        numero=3,
    )

    with secao_tabela:
        if erro_baixo_desempenho is not None:
            st.warning(
                "Não foi possível carregar a lista de acompanhamento."
            )
        elif baixo_desempenho.empty:
            renderizarEstadoVazio(
                "Nenhum aluno atende aos critérios de baixo desempenho."
            )
        else:
            tabela = baixo_desempenho.sort_values(
                by=["CR", "Reprovações"],
                ascending=[True, False],
                na_position="last",
            )

            st.dataframe(
                tabela,
                hide_index=True,
                use_container_width=True,
                row_height=38,
                column_config={
                    "Aluno": st.column_config.TextColumn(
                        "Aluno",
                        width="large",
                    ),
                    "Matrícula": st.column_config.TextColumn(
                        "Matrícula",
                    ),
                    "Curso": st.column_config.TextColumn(
                        "Curso",
                        width="medium",
                    ),
                    "Campus": st.column_config.TextColumn(
                        "Campus",
                    ),
                    "CR": st.column_config.ProgressColumn(
                        "CR",
                        format="%.2f",
                        min_value=0,
                        max_value=10,
                    ),
                    "Reprovações": st.column_config.NumberColumn(
                        "Reprovações",
                        format="%d",
                    ),
                },
            )