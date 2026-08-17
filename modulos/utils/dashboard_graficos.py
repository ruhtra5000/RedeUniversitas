from __future__ import annotations
from typing import Any
import altair as alt
import pandas as pd
import streamlit as st

# Configuração visual única para manter todos os gráficos alinhados
ALTURA_GRAFICO = 165
ESPESSURA_BARRA = 18
LIMITE_ROTULO_GRAFICO = 190

# Função para renderizar o rótulo de um gráfico com título e descrição
def rotuloGrafico(titulo: str, descricao: str | None = None) -> None:

    complemento = (
        f"""
        <div style="
            color:#64748B;
            font-size:0.68rem;
            margin-top:0.12rem;
        ">
            {descricao}
        </div>
        """
        if descricao
        else ""
    )

    st.html(
        f"""
        <div style="
            margin-top:0.35rem;
            margin-bottom:-0.15rem;
        ">
            <div style="
                color:#8190A4;
                font-size:0.62rem;
                font-weight:800;
                letter-spacing:0.08em;
                text-transform:uppercase;
            ">
                {titulo}
            </div>

            {complemento}
        </div>
        """
    )

# Função para configurar o eixo de categoria de um gráfico
def eixoCategoriaGrafico(campo: str, ordem: list[str] | None = None) -> alt.Y:

    return alt.Y(
        f"{campo}:N",
        sort=ordem,
        title=None,
        axis=alt.Axis(
            labelColor="#8FA0B6",
            labelFontSize=10,
            labelPadding=10,
            labelLimit=LIMITE_ROTULO_GRAFICO,
            ticks=False,
            domain=False,
        ),
    )

# Função para configurar o eixo de valor de um gráfico
def eixoValorGrafico(campo: str, *, inteiro: bool = False, limite: float | None = None, percentual: bool = False) -> alt.X:

    configuracaoEixo: dict[str, Any] = {
        "labelColor": "#66778D",
        "labelFontSize": 9,
        "labelPadding": 6,
        "tickCount": 6,
        "grid": True,
        "gridColor": "rgba(148,163,184,0.08)",
        "ticks": False,
        "domain": False,
    }

    if percentual:
        configuracaoEixo["labelExpr"] = "datum.value + '%'"
    elif inteiro:
        configuracaoEixo["format"] = "d"
        configuracaoEixo["tickMinStep"] = 1
    else:
        configuracaoEixo["format"] = "~s"

    escala = (
        alt.Scale(
            domain=[0, limite],
            nice=False,
        )
        if limite is not None
        else alt.Scale(
            zero=True
        )
    )

    return alt.X(
        f"{campo}:Q",
        title=None,
        scale=escala,
        axis=alt.Axis(
            **configuracaoEixo
        ),
    )

# Função para finalizar a configuração de um gráfico e renderizá-lo no Streamlit
def finalizarGrafico(grafico: alt.Chart, titulo: str, descricao: str | None = None) -> None:

    grafico = (
        grafico
        .properties(
            height=ALTURA_GRAFICO
        )
        .configure_view(
            stroke=None
        )
        .configure(
            background="transparent"
        )
    )

    rotuloGrafico(
        titulo,
        descricao,
    )

    st.altair_chart(
        grafico,
        use_container_width=True,
        theme=None,
    )

# Função compartilhada para renderizar barras horizontais no padrão do dashboard operacional
def renderizarGraficoBarras(
    dados: pd.DataFrame,
    *,
    categoria: str,
    valor: str,
    titulo: str,
    ordem: list[str] | None = None,
    cor: str | None = None,
    cores: dict[str, str] | None = None,
    inteiro: bool = False,
    limite: float | None = None,
    percentual: bool = False,
    tooltip: list[Any] | None = None,
    descricao: str | None = None,
) -> None:

    if cores:
        codificacaoCor = alt.Color(
            f"{categoria}:N",
            scale=alt.Scale(
                domain=list(cores.keys()),
                range=list(cores.values()),
            ),
            legend=None,
        )
    else:
        codificacaoCor = alt.value(
            cor or "#54a3c7"
        )

    grafico = (
        alt.Chart(dados)
        .mark_bar(
            cornerRadiusTopRight=5,
            cornerRadiusBottomRight=5,
            size=ESPESSURA_BARRA,
        )
        .encode(
            y=eixoCategoriaGrafico(
                categoria,
                ordem,
            ),
            x=eixoValorGrafico(
                valor,
                inteiro=inteiro,
                limite=limite,
                percentual=percentual,
            ),
            color=codificacaoCor,
            tooltip=tooltip or [],
        )
    )

    finalizarGrafico(
        grafico,
        titulo,
        descricao,
    )