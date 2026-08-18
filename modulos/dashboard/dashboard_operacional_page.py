from __future__ import annotations
import unicodedata
from collections.abc import Mapping
from datetime import date, datetime
from typing import Any
import altair as alt
import pandas as pd
import streamlit as st
from modulos.dashboard import dashboard_service
from modulos.utils.dashboard_visual import (MetricaDashboard, criarSecaoDashboard, formatarInteiro, paraNumero, renderizarCabecalhoDashboard, renderizarEstadoVazio, renderizarMetricasDashboard)
import modulos.utils.dashboard_graficos as dashboard_graficos
from modulos.dashboard.dashboard_geral_page import obterCampusIdUsuario

# Cores
COR_ESTOQUE = "#54a3c7"
COR_BAIXO = "#d4a84f"
COR_SEM_ESTOQUE = "#cf6871"
COR_COMPRA = "#6f8fd3"
COR_FORNECEDOR = "#8d7fd1"
CORvalor = "#54b68a"

# Cores para os tipos de movimentação
CORES_MOVIMENTACAO = {
    "Entrada": "#54b68a",
    "Saída": "#6f8fd3",
    "Ajuste": "#d4a84f",
    "Perda": "#cf6871",
}

# Função para formatar valores monetários
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

# Função para normalizar chaves de dicionário ou atributos
def normalizarChave(valor: Any) -> str:
    texto = unicodedata.normalize(
        "NFKD",
        str(valor or ""),
    )

    texto = "".join(
        caractere
        for caractere in texto
        if not unicodedata.combining(caractere)
    )

    return (
        texto
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )

# Função para obter o texto de um valor de enumeração ou string
def textoEnum(valor: Any) -> str:
    if valor is None:
        return ""

    if hasattr(valor, "value"):
        valor = valor.value

    elif hasattr(valor, "name"):
        valor = valor.name

    chave = normalizarChave(valor)

    nomes = {
        "entrada": "Entrada",
        "saida": "Saída",
        "ajuste": "Ajuste",
        "perda": "Perda",
    }

    return nomes.get(
        chave,
        str(valor)
        .replace("_", " ")
        .title(),
    )

# Função para mapear um registro para um dicionário
def mapping(registro: Any) -> dict[str, Any]:
    if isinstance(registro, Mapping):
        return dict(registro)

    if hasattr(registro, "_mapping"):
        return dict(registro._mapping)

    if hasattr(registro, "mapping"):
        return dict(registro.mapping)

    return {}

# Função para obter o valor de um atributo de um objeto
def valorAtributo(objeto: Any, nome: str) -> Any:
    try:
        return getattr(
            objeto,
            nome,
            None,
        )

    except Exception:
        return None

# Função para obter o valor de um registro com base em nomes de campos ou atributos
def valorRegistro(registro: Any, *nomes: str) -> Any:

    nomes_normalizados = {
        normalizarChave(nome)
        for nome in nomes
    }

    dados = mapping(
        registro
    )

    for chave, valor in dados.items():

        if (
            normalizarChave(chave)
            in nomes_normalizados
        ):
            return valor

    for nome in nomes:

        valor = valorAtributo(
            registro,
            nome,
        )

        if valor is not None:
            return valor

    for relacionamento in (
        "produto",
        "estoque",
        "fornecedor",
        "compra",
        "movimentacao",
    ):

        objeto = valorAtributo(
            registro,
            relacionamento,
        )

        if objeto is None and dados:

            for chave, valor in dados.items():

                if (
                    normalizarChave(chave)
                    == relacionamento
                ):
                    objeto = valor
                    break

        if objeto is None:
            continue

        subdados = mapping(
            objeto
        )

        for chave, valor in subdados.items():

            if (
                normalizarChave(chave)
                in nomes_normalizados
            ):
                return valor

        for nome in nomes:

            valor = valorAtributo(
                objeto,
                nome,
            )

            if valor is not None:
                return valor

    return None

# Função para listar registros a partir de diferentes tipos de dados
def listarRegistros(dados: Any) -> list[Any]:

    if dados is None:
        return []

    if isinstance(
        dados,
        pd.DataFrame,
    ):
        return dados.to_dict(
            "records"
        )

    if isinstance(
        dados,
        Mapping,
    ):
        return [dados]

    if isinstance(
        dados,
        (list, tuple),
    ):
        return list(dados)

    return [dados]

# Função para obter valores sequenciais de um registro
def valoresSequenciais(registro: Any) -> list[Any]:

    mapeamento = mapping(
        registro
    )

    if mapeamento:
        return list(
            mapeamento.values()
        )

    if isinstance(
        registro,
        (list, tuple),
    ):
        return list(registro)

    try:

        if not isinstance(
            registro,
            (
                str,
                bytes,
                Mapping,
            ),
        ):
            return list(registro)

    except Exception:
        pass

    return []

# Função para obter valores numéricos sequenciais de um registro
def numericosSequenciais(registro: Any) -> list[float]:

    numeros = []

    for valor in valoresSequenciais(
        registro
    ):

        if isinstance(
            valor,
            bool,
        ):
            continue

        if isinstance(
            valor,
            (int, float),
        ):

            numeros.append(
                float(valor)
            )

            continue

        try:

            if (
                valor is not None
                and valor.__class__.__module__
                == "decimal"
            ):

                numeros.append(
                    float(valor)
                )

        except Exception:
            pass

    return numeros

# Função para normalizar produtos críticos (baixo estoque e sem estoque) em um DataFrame
def normalizarProdutosCriticos(baixo: Any, sem: Any) -> pd.DataFrame:

    itens: dict[
        tuple[str, str],
        dict[str, Any],
    ] = {}

    def adicionar(
        registro: Any,
        situacao: str,
    ) -> None:

        produto = valorRegistro(
            registro,
            "produto",
        )

        nome = valorRegistro(
            registro,
            "produto_nome",
            "nome_produto",
            "nome",
        )

        marca = valorRegistro(
            registro,
            "marca",
            "produto_marca",
        )

        if (
            produto is not None
            and not isinstance(
                produto,
                (
                    str,
                    int,
                    float,
                    bool,
                ),
            )
        ):

            nome = (
                valorAtributo(
                    produto,
                    "nome",
                )
                or nome
            )

            marca = (
                valorAtributo(
                    produto,
                    "marca",
                )
                or marca
            )

        quantidade = valorRegistro(
            registro,
            "quantidade",
            "qtde",
            "qtd",
            "quantidade_estoque",
            "saldo",
        )

        minimo = valorRegistro(
            registro,
            "estoque_minimo",
            "quantidade_minima",
            "quantidade_min",
            "qtde_minima",
            "qtde_min",
            "qtd_minima",
            "qtd_min",
            "minimo",
        )

        item = {
            "Produto": (
                nome
                or "Não informado"
            ),

            "Marca": (
                marca
                or "Não informada"
            ),

            "Quantidade": int(
                round(
                    paraNumero(
                        quantidade
                    )
                )
            ),

            "Mínimo": (
                int(
                    round(
                        paraNumero(
                            minimo
                        )
                    )
                )
                if minimo is not None
                else None
            ),

            "Situação": situacao,
        }

        itens[
            (
                item["Produto"],
                item["Marca"],
            )
        ] = item

    for registro in listarRegistros(
        baixo
    ):

        adicionar(
            registro,
            "Baixo estoque",
        )

    for registro in listarRegistros(
        sem
    ):

        adicionar(
            registro,
            "Sem estoque",
        )

    return pd.DataFrame(
        list(
            itens.values()
        ),

        columns=[
            "Produto",
            "Marca",
            "Quantidade",
            "Mínimo",
            "Situação",
        ],
    )

# Função para normalizar produtos mais usados em um DataFrame
def normalizarProdutosMaisUsados(dados: Any) -> pd.DataFrame:

    linhas = []

    for registro in listarRegistros(
        dados
    ):

        produto = valorRegistro(
            registro,
            "produto",
        )

        nome = valorRegistro(
            registro,
            "produto_nome",
            "nome_produto",
            "nome",
        )

        marca = valorRegistro(
            registro,
            "marca",
            "produto_marca",
        )

        if (
            produto is not None
            and not isinstance(
                produto,
                (
                    str,
                    int,
                    float,
                    bool,
                ),
            )
        ):

            nome = (
                valorAtributo(
                    produto,
                    "nome",
                )
                or nome
            )

            marca = (
                valorAtributo(
                    produto,
                    "marca",
                )
                or marca
            )

        movimentacoes = valorRegistro(
            registro,
            "quantidade_movimentacoes",
            "qtde_movimentacoes",
            "qtd_movimentacoes",
            "movimentacoes",
            "quantidade_saidas",
            "qtde_saidas",
            "qtd_saidas",
            "saidas",
            "quantidade",
            "total",
            "contagem",
            "count",
        )

        sequencia = valoresSequenciais(
            registro
        )

        numeros = numericosSequenciais(
            registro
        )

        if nome is None and sequencia:

            for valor in sequencia:

                if isinstance(
                    valor,
                    str,
                ):
                    nome = valor
                    break

        if marca is None and sequencia:

            textos = [
                valor
                for valor in sequencia
                if isinstance(
                    valor,
                    str,
                )
            ]

            if len(textos) >= 2:
                marca = textos[1]

        if (
            movimentacoes is None
            and numeros
        ):
            movimentacoes = numeros[-1]

        linhas.append(
            {
                "Produto": str(
                    nome
                    or "Não informado"
                ),

                "Marca": str(
                    marca
                    or "Não informada"
                ),

                "Movimentações": int(
                    round(
                        paraNumero(
                            movimentacoes
                        )
                    )
                ),
            }
        )

    df = pd.DataFrame(
        linhas,

        columns=[
            "Produto",
            "Marca",
            "Movimentações",
        ],
    )

    if not df.empty:

        df = (
            df
            .sort_values(
                "Movimentações",
                ascending=False,
            )
            .head(5)
        )

    return df

# Função para normalizar movimentações por tipo em um DataFrame
def normalizarMovimentacoesTipo(dados: Any) -> pd.DataFrame:

    linhas = []

    for registro in listarRegistros(
        dados
    ):

        tipo = valorRegistro(
            registro,
            "tipo",
            "tipo_movimentacao",
            "status",
        )

        movimentos = valorRegistro(
            registro,
            "quantidade_movimentacoes",
            "qtde_movimentacoes",
            "qtd_movimentacoes",
            "movimentacoes",
            "total_movimentacoes",
            "contagem",
            "count",
        )

        unidades = valorRegistro(
            registro,
            "quantidade_unidades",
            "qtde_unidades",
            "qtd_unidades",
            "unidades",
            "unidades_movimentadas",
            "total_unidades",
            "quantidade_total",
            "soma_quantidade",
        )

        sequencia = valoresSequenciais(
            registro
        )

        numeros = numericosSequenciais(
            registro
        )

        if tipo is None and sequencia:

            for valor in sequencia:

                if (
                    isinstance(
                        valor,
                        str,
                    )
                    or hasattr(
                        valor,
                        "name",
                    )
                    or hasattr(
                        valor,
                        "value",
                    )
                ):

                    tipo = valor
                    break

        if (
            movimentos is None
            and numeros
        ):
            movimentos = numeros[0]

        if unidades is None:

            if len(numeros) >= 2:
                unidades = numeros[1]

            elif numeros:
                unidades = numeros[0]

        linhas.append(
            {
                "Tipo": (
                    textoEnum(tipo)
                    or "Não informado"
                ),

                "Movimentações": int(
                    round(
                        paraNumero(
                            movimentos
                        )
                    )
                ),

                "Unidades": int(
                    round(
                        paraNumero(
                            unidades
                        )
                    )
                ),
            }
        )

    return pd.DataFrame(
        linhas,

        columns=[
            "Tipo",
            "Movimentações",
            "Unidades",
        ],
    )

# Função para normalizar períodos em formato de data ou string
def normalizarPeriodo(valor: Any) -> str:

    if valor is None:
        return "Não informado"

    if isinstance(
        valor,
        (
            date,
            datetime,
            pd.Timestamp,
        ),
    ):

        return pd.Timestamp(
            valor
        ).strftime(
            "%m/%Y"
        )

    texto = str(
        valor
    ).strip()

    try:

        return pd.to_datetime(
            texto
        ).strftime(
            "%m/%Y"
        )

    except Exception:
        return texto

# Função para normalizar movimentações recentes em um DataFrame
def normalizarMovimentacoesRecentes(dados: Any) -> pd.DataFrame:

    linhas = []

    for registro in listarRegistros(
        dados
    ):

        periodo = valorRegistro(
            registro,
            "mes",
            "mês",
            "periodo",
            "data",
            "mes_ano",
        )

        tipo = valorRegistro(
            registro,
            "tipo",
            "tipo_movimentacao",
            "status",
        )

        quantidade = valorRegistro(
            registro,
            "quantidade",
            "qtde",
            "qtd",
            "movimentacoes",
            "quantidade_movimentacoes",
            "total",
        )

        if (
            isinstance(
                registro,
                (list, tuple),
            )
            and not mapping(
                registro
            )
        ):

            if len(registro) > 0:
                periodo = registro[0]

            if len(registro) > 1:
                tipo = registro[1]

            if len(registro) > 2:
                quantidade = registro[2]

        linhas.append(
            {
                "Período": (
                    normalizarPeriodo(
                        periodo
                    )
                ),

                "Tipo": (
                    textoEnum(tipo)
                    or "Não informado"
                ),

                "Movimentações": int(
                    round(
                        paraNumero(
                            quantidade
                        )
                    )
                ),
            }
        )

    return pd.DataFrame(
        linhas,

        columns=[
            "Período",
            "Tipo",
            "Movimentações",
        ],
    )

# Função para normalizar produtos mais comprados em um DataFrame
def normalizarProdutosComprados(dados: Any) -> pd.DataFrame:

    linhas = []

    for registro in listarRegistros(
        dados
    ):

        produto = valorRegistro(
            registro,
            "produto",
        )

        nome = valorRegistro(
            registro,
            "produto_nome",
            "nome_produto",
            "nome",
        )

        marca = valorRegistro(
            registro,
            "marca",
            "produto_marca",
        )

        if (
            produto is not None
            and not isinstance(
                produto,
                (
                    str,
                    int,
                    float,
                    bool,
                ),
            )
        ):

            nome = (
                valorAtributo(
                    produto,
                    "nome",
                )
                or nome
            )

            marca = (
                valorAtributo(
                    produto,
                    "marca",
                )
                or marca
            )

        unidades = valorRegistro(
            registro,
            "unidades_compradas",
            "quantidade_comprada",
            "qtde_comprada",
            "qtd_comprada",
            "quantidade_total",
            "qtde_total",
            "qtd_total",
            "unidades",
            "quantidade",
        )

        valor = valorRegistro(
            registro,
            "valor_gasto",
            "total_gasto",
            "valor_total_gasto",
            "valor_total",
            "total_comprado",
            "total",
            "valor",
        )

        sequencia = valoresSequenciais(
            registro
        )

        numeros = numericosSequenciais(
            registro
        )

        if nome is None and sequencia:

            for item in sequencia:

                if isinstance(
                    item,
                    str,
                ):
                    nome = item
                    break

        if marca is None and sequencia:

            textos = [
                item
                for item in sequencia
                if isinstance(
                    item,
                    str,
                )
            ]

            if len(textos) >= 2:
                marca = textos[1]

        if (
            unidades is None
            and numeros
        ):
            unidades = numeros[0]

        if valor is None:

            if len(numeros) >= 2:
                valor = numeros[-1]

            else:
                valor = 0

        linhas.append(
            {
                "Produto": str(
                    nome
                    or "Não informado"
                ),

                "Marca": str(
                    marca
                    or "Não informada"
                ),

                "Unidades": int(
                    round(
                        paraNumero(
                            unidades
                        )
                    )
                ),

                "Valor gasto": (
                    paraNumero(
                        valor
                    )
                ),
            }
        )

    df = pd.DataFrame(
        linhas,

        columns=[
            "Produto",
            "Marca",
            "Unidades",
            "Valor gasto",
        ],
    )

    if not df.empty:

        if float(
            df[
                "Valor gasto"
            ].sum()
        ) > 0:

            df = df.sort_values(
                "Valor gasto",
                ascending=False,
            )

        else:

            df = df.sort_values(
                "Unidades",
                ascending=False,
            )

        df = df.head(5)

    return df

# Função para normalizar fornecedores mais usados em um DataFrame
def normalizarFornecedores(dados: Any) -> pd.DataFrame:

    linhas = []

    for registro in listarRegistros(
        dados
    ):

        nome = None
        compras = None
        valor = None

        fornecedor = valorRegistro(
            registro,
            "fornecedor",
        )

        nome = valorRegistro(
            registro,
            "fornecedor_nome",
            "nome_fornecedor",
            "nome",
        )

        if (
            fornecedor is not None
            and not isinstance(
                fornecedor,
                (
                    str,
                    int,
                    float,
                    bool,
                ),
            )
        ):

            nome = (
                valorAtributo(
                    fornecedor,
                    "nome",
                )
                or nome
            )

        compras = valorRegistro(
            registro,
            "quantidade_vendas",
            "qtde_vendas",
            "qtd_vendas",
            "quantidade_compras",
            "qtde_compras",
            "qtd_compras",
            "numero_compras",
            "total_compras",
            "compras",
            "vendas",
            "quantidade",
            "contagem",
            "count",
        )

        valor = valorRegistro(
            registro,
            "valor_gasto",
            "total_gasto",
            "valor_total_gasto",
            "valor_total",
            "total_comprado",
            "total",
            "valor",
        )

        sequencia = valoresSequenciais(
            registro
        )

        numeros = numericosSequenciais(
            registro
        )

        if nome is None and sequencia:

            for item in sequencia:

                nomeObjeto = valorAtributo(
                    item,
                    "nome",
                )

                if nomeObjeto:
                    nome = nomeObjeto
                    break

                if isinstance(
                    item,
                    str,
                ):
                    nome = item
                    break

        if (
            compras is None
            and numeros
        ):
            compras = numeros[0]

        if valor is None:

            if len(numeros) >= 2:
                valor = numeros[-1]

            else:
                valor = 0

        linhas.append(
            {
                "Fornecedor": str(
                    nome
                    or "Não informado"
                ),

                "Compras": int(
                    round(
                        paraNumero(
                            compras
                        )
                    )
                ),

                "Valor gasto": (
                    paraNumero(
                        valor
                    )
                ),
            }
        )

    df = pd.DataFrame(
        linhas,

        columns=[
            "Fornecedor",
            "Compras",
            "Valor gasto",
        ],
    )

    if not df.empty:

        if float(
            df[
                "Valor gasto"
            ].sum()
        ) > 0:

            df = df.sort_values(
                "Valor gasto",
                ascending=False,
            )

        else:

            df = df.sort_values(
                "Compras",
                ascending=False,
            )

        df = df.head(5)

    return df

@st.cache_data(ttl=60, show_spinner=False)
# Função para carregar indicadores operacionais do dashboard, com suporte a filtro por campus.
def carregarIndicadoresOperacionais(campus_id: int | None = None) -> dict[str, Any]:

    if campus_id is None:
        return {
            "tipos_produtos": paraNumero(
                dashboard_service.tipoProdutosGeral()
            ),

        "quantidade_produtos": paraNumero(
            dashboard_service.qtdeProdutosGeral()
        ),

        "baixo_estoque": paraNumero(
            dashboard_service.qtdeProdutosBaixoEstoqueGeral()
        ),

        "sem_estoque": paraNumero(
            dashboard_service.qtdeProdutosSemEstoqueGeral()
        ),

        "lista_baixo": (
            dashboard_service
            .listarProdutosBaixoEstoqueGeral()
        ),

        "lista_sem": (
            dashboard_service
            .listarProdutosSemEstoqueGeral()
        ),

        "mais_usados": (
            dashboard_service
            .produtosMaisUsadosGeral()
        ),

        "movimentacoes_tipo": (
            dashboard_service
            .movimentacoesPorTipoGeral()
        ),

        "movimentacoes_recentes": (
            dashboard_service
            .movimentacoesRecentesGeral()
        ),

        "compras": paraNumero(
            dashboard_service
            .qtdeComprasGeral()
        ),

        "valor_comprado": paraNumero(
            dashboard_service
            .valorTotalCompradoGeral()
        ),

        "ticket_medio": paraNumero(
            dashboard_service
            .valorMedioCompraGeral()
        ),

        "mais_comprados": (
            dashboard_service
            .produtosMaisCompradosGeral()
        ),

        "fornecedores": paraNumero(
            dashboard_service
            .qtdeFornecedores()
        ),

            "fornecedores_usados": (
                dashboard_service
                .fornecedoresMaisUsadosGeral()
            ),
        }
    else:
        return {
            "tipos_produtos": paraNumero(
                dashboard_service.tipoProdutosPorCampus(campus_id)
            ),

            "quantidade_produtos": paraNumero(
                dashboard_service.qtdeProdutosPorCampus(campus_id)
            ),

            "baixo_estoque": paraNumero(
                dashboard_service.qtdeProdutosBaixoEstoquePorCampus(campus_id)
            ),

            "sem_estoque": paraNumero(
                dashboard_service.qtdeProdutosSemEstoquePorCampus(campus_id)
            ),

            "lista_baixo": (
                dashboard_service
                .listarProdutosBaixoEstoquePorCampus(campus_id)
            ),

            "lista_sem": (
                dashboard_service
                .listarProdutosSemEstoquePorCampus(campus_id)
            ),

            "mais_usados": (
                dashboard_service
                .produtosMaisUsadosPorCampus(campus_id)
            ),

            "movimentacoes_tipo": (
                dashboard_service
                .movimentacoesPorTipoPorCampus(campus_id)
            ),

            "movimentacoes_recentes": (
                dashboard_service
                .movimentacoesRecentesPorCampus(campus_id)
            ),

            "compras": paraNumero(
                dashboard_service
                .qtdeComprasPorCampus(campus_id)
            ),

            "valor_comprado": paraNumero(
                dashboard_service
                .valorTotalCompradoPorCampus(campus_id)
            ),

            "ticket_medio": paraNumero(
                dashboard_service
                .valorMedioCompraPorCampus(campus_id)
            ),

            "mais_comprados": (
                dashboard_service
                .produtosMaisCompradosPorCampus(campus_id)
            ),

            "fornecedores": paraNumero(
                dashboard_service
                .qtdeFornecedores()
            ),

            "fornecedores_usados": (
                dashboard_service
                .fornecedoresMaisUsadosPorCampus(campus_id)
            ),
        }

# Função para renderizar o rótulo de um gráfico com título e descrição
def rotuloGrafico(titulo: str, descricao: str | None = None) -> None:
    return dashboard_graficos.rotuloGrafico(
        titulo,
        descricao,
    )

# Configuração visual única para manter todos os gráficos alinhados
ALTURA_GRAFICO = dashboard_graficos.ALTURA_GRAFICO
ESPESSURA_BARRA = dashboard_graficos.ESPESSURA_BARRA
LARGURA_EIXO_CATEGORIA = 170
LIMITE_ROTULO_GRAFICO = 150

# Função para configurar o eixo de categoria de um gráfico 
def eixoCategoriaGrafico(campo: str, ordem: list[str] | None = None) -> alt.Y:
    return dashboard_graficos.eixoCategoriaGrafico(
        campo,
        ordem,
    )

# Função para configurar o eixo de valor de um gráfico 
def eixoValorGrafico(campo: str, *, inteiro: bool = False, limite: float | None = None) -> alt.X:
    return dashboard_graficos.eixoValorGrafico(
        campo,
        inteiro=inteiro,
        limite=limite,
    )

# Função para finalizar a configuração de um gráfico e renderizá-lo no Streamlit
def finalizarGrafico(grafico: alt.Chart, titulo: str, descricao: str | None = None) -> None:
    return dashboard_graficos.finalizarGrafico(
        grafico,
        titulo,
        descricao,
    )

# Função para criar um gráfico de ranking com base em dados fornecidos
def graficoRanking(dados: pd.DataFrame, *, categoria: str, valor: str, titulo: str, cor: str, monetario: bool = False, tooltip_extra: list[str] | None = None, limite_grafico: float | None = None,) -> bool:

    if dados.empty or valor not in dados.columns:
        return False

    tabela = dados.copy()
    tabela[valor] = tabela[valor].apply(paraNumero)
    tabela = tabela[tabela[valor] > 0]

    if tabela.empty:
        return False

    tabela = (
        tabela
        .sort_values(valor, ascending=False)
        .head(5)
        .copy()
    )

    tabela["Valor exibido"] = (
        tabela[valor].apply(formatarMoeda)
        if monetario
        else tabela[valor].apply(formatarInteiro)
    )

    ordem = tabela[categoria].tolist()

    tooltips = [
        alt.Tooltip(
            f"{categoria}:N",
            title=categoria,
        ),
        alt.Tooltip(
            "Valor exibido:N",
            title=(
                "Valor"
                if monetario
                else valor
            ),
        ),
    ]

    for campo in tooltip_extra or []:
        if campo not in tabela.columns:
            continue

        if campo == "Valor gasto":
            tabela["Valor gasto formatado"] = tabela[campo].apply(formatarMoeda)
            tooltips.append(
                alt.Tooltip(
                    "Valor gasto formatado:N",
                    title="Valor gasto",
                )
            )
        else:
            tooltips.append(
                alt.Tooltip(
                    f"{campo}:Q",
                    title=campo,
                )
            )

    grafico = (
        alt.Chart(tabela)
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
            x=eixoValorGrafico(valor, limite=limite_grafico),
            color=alt.value(cor),
            tooltip=tooltips,
        )
    )

    finalizarGrafico(
        grafico,
        titulo,
    )

    return True

# Função para criar um gráfico de estoque com base em produtos com baixo estoque e sem estoque
def graficoEstoque(baixo: int, sem: int) -> bool:

    dados = pd.DataFrame(
        {
            "Situação": [
                "Baixo estoque",
                "Sem estoque",
            ],
            "Produtos": [
                max(baixo, 0),
                max(sem, 0),
            ],
        }
    )

    if int(dados["Produtos"].sum()) <= 0:
        return False

    ordem = [
        "Baixo estoque",
        "Sem estoque",
    ]

    grafico = (
        alt.Chart(dados)
        .mark_bar(
            cornerRadiusTopRight=5,
            cornerRadiusBottomRight=5,
            size=ESPESSURA_BARRA,
        )
        .encode(
            y=eixoCategoriaGrafico(
                "Situação",
                ordem,
            ),
            x=eixoValorGrafico(
                "Produtos",
                inteiro=True,
            ),
            color=alt.Color(
                "Situação:N",
                scale=alt.Scale(
                    domain=ordem,
                    range=[
                        COR_BAIXO,
                        COR_SEM_ESTOQUE,
                    ],
                ),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip(
                    "Situação:N",
                    title="Situação",
                ),
                alt.Tooltip(
                    "Produtos:Q",
                    title="Produtos",
                    format=".0f",
                ),
            ],
        )
    )

    finalizarGrafico(
        grafico,
        "Comparativo visual",
    )

    return True

# Função para criar um gráfico de produtos mais utilizados com base em dados fornecidos
def graficoProdutosUsados(dados: pd.DataFrame) -> bool:

    if dados.empty:
        return False

    tabela = dados.copy()

    tabela["Produto"] = (
        tabela["Produto"].astype(str)
        + " · "
        + tabela["Marca"].astype(str)
    )

    return graficoRanking(
        tabela,
        categoria="Produto",
        valor="Movimentações",
        titulo="Produtos mais utilizados",
        cor=COR_ESTOQUE,
    )

# Função para criar um gráfico de movimentações por tipo com base em dados fornecidos
def graficoMovimentacoesTipo(dados: pd.DataFrame) -> bool:

    if dados.empty:
        return False

    tabela = dados.copy()
    tabela["Movimentações"] = tabela["Movimentações"].apply(paraNumero)
    tabela["Unidades"] = tabela["Unidades"].apply(paraNumero)
    tabela = tabela[tabela["Unidades"] > 0]

    if tabela.empty:
        return False

    ordem = [
        tipo
        for tipo in [
            "Entrada",
            "Saída",
            "Ajuste",
            "Perda",
        ]
        if tipo in tabela["Tipo"].values
    ]

    grafico = (
        alt.Chart(tabela)
        .mark_bar(
            cornerRadiusTopRight=5,
            cornerRadiusBottomRight=5,
            size=ESPESSURA_BARRA,
        )
        .encode(
            y=eixoCategoriaGrafico(
                "Tipo",
                ordem,
            ),
            x=eixoValorGrafico("Unidades"),
            color=alt.Color(
                "Tipo:N",
                scale=alt.Scale(
                    domain=[
                        "Entrada",
                        "Saída",
                        "Ajuste",
                        "Perda",
                    ],
                    range=[
                        CORES_MOVIMENTACAO["Entrada"],
                        CORES_MOVIMENTACAO["Saída"],
                        CORES_MOVIMENTACAO["Ajuste"],
                        CORES_MOVIMENTACAO["Perda"],
                    ],
                ),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip(
                    "Tipo:N",
                    title="Tipo",
                ),
                alt.Tooltip(
                    "Unidades:Q",
                    title="Unidades movimentadas",
                    format=".0f",
                ),
                alt.Tooltip(
                    "Movimentações:Q",
                    title="Movimentações",
                    format=".0f",
                ),
            ],
        )
    )

    finalizarGrafico(
        grafico,
        "Comparativo visual",
    )

    return True

# Função para criar um gráfico de movimentações recentes com base em dados fornecidos
def graficoMovimentacoesRecentes(dados: pd.DataFrame) -> bool:

    if dados.empty:
        return False

    tabela = dados.copy()
    tabela["Movimentações"] = tabela["Movimentações"].apply(paraNumero)
    tabela = tabela[tabela["Movimentações"] > 0]

    if tabela.empty:
        return False

    mensal = (
        tabela
        .groupby(
            "Período",
            as_index=False,
        )
        .agg(
            Volume=(
                "Movimentações",
                "sum",
            )
        )
    )

    if len(mensal) < 2:
        return False

    mensal["DataOrdenacao"] = pd.to_datetime(
        "01/" + mensal["Período"],
        format="%d/%m/%Y",
        errors="coerce",
    )

    mensal = mensal.sort_values("DataOrdenacao")
    ordem = mensal["Período"].tolist()

    grafico = (
        alt.Chart(mensal)
        .mark_bar(
            cornerRadiusTopRight=5,
            cornerRadiusBottomRight=5,
            size=ESPESSURA_BARRA,
        )
        .encode(
            y=eixoCategoriaGrafico(
                "Período",
                ordem,
            ),
            x=eixoValorGrafico(
                "Volume",
                inteiro=True,
            ),
            color=alt.value(COR_ESTOQUE),
            tooltip=[
                alt.Tooltip(
                    "Período:N",
                    title="Período",
                ),
                alt.Tooltip(
                    "Volume:Q",
                    title="Movimentações",
                    format=".0f",
                ),
            ],
        )
    )

    finalizarGrafico(
        grafico,
        "Evolução das movimentações",
    )

    return True

# Função para criar um gráfico de produtos mais comprados com base em dados fornecidos
def graficoProdutosComprados(dados: pd.DataFrame, limite_grafico: float | None = None) -> bool:

    if dados.empty:
        return False

    tabela = dados.copy()

    tabela["Produto"] = (
        tabela["Produto"].astype(str)
        + " · "
        + tabela["Marca"].astype(str)
    )

    valor_total = float(
        tabela["Valor gasto"].apply(paraNumero).sum()
    )

    unidades_total = float(
        tabela["Unidades"].apply(paraNumero).sum()
    )

    if valor_total > 0:
        return graficoRanking(
            tabela,
            categoria="Produto",
            valor="Valor gasto",
            titulo="Produtos com maior gasto",
            cor=COR_COMPRA,
            monetario=True,
            tooltip_extra=[
                "Unidades"
            ],
            limite_grafico=limite_grafico
        )

    if unidades_total > 0:
        return graficoRanking(
            tabela,
            categoria="Produto",
            valor="Unidades",
            titulo="Produtos mais comprados",
            cor=COR_COMPRA,
            tooltip_extra=[
                "Valor gasto"
            ],
            limite_grafico=limite_grafico
        )

    return False

# Função para criar um gráfico de fornecedores mais utilizados com base em dados fornecidos
def graficoFornecedores(dados: pd.DataFrame, limite_grafico: float | None = None) -> bool:

    if dados.empty:
        return False

    tabela = dados.copy()

    valor_total = float(
        tabela["Valor gasto"].apply(paraNumero).sum()
    )

    compras_total = float(
        tabela["Compras"].apply(paraNumero).sum()
    )

    if valor_total > 0:
        return graficoRanking(
            tabela,
            categoria="Fornecedor",
            valor="Valor gasto",
            titulo="Participação dos fornecedores",
            cor=COR_FORNECEDOR,
            monetario=True,
            tooltip_extra=[
                "Compras"
            ],
            limite_grafico=limite_grafico
        )

    if compras_total > 0:
        return graficoRanking(
            tabela,
            categoria="Fornecedor",
            valor="Compras",
            titulo="Fornecedores mais utilizados",
            cor=COR_FORNECEDOR,
            tooltip_extra=[
                "Valor gasto"
            ],
            limite_grafico=limite_grafico
        )

    return False

# Função principal para renderizar a tela do dashboard operacional
def telaDashboardOperacional():
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
        titulo="Operacional",

        descricao=(
            "Visão do estoque, movimentações, compras "
            "e fornecedores da Rede Universitas." if campus_nome is None else
            f"Visão do estoque, movimentações, compras e fornecedores ({campus_nome})."
        ),

        prefixo_chave=(
            "dashboard_operacional"
        ),
    )

    if atualizar:
        carregarIndicadoresOperacionais.clear()

    try:

        with st.spinner(
            "Carregando indicadores..."
        ):

            dados = (
                carregarIndicadoresOperacionais(campus_id)
            )

    except Exception as erro:

        st.error(
            "Não foi possível carregar "
            "os indicadores operacionais."
        )

        st.caption(
            f"Detalhes técnicos: {erro}"
        )

        return

    tipos_produtos = int(
        dados[
            "tipos_produtos"
        ]
    )

    quantidade_produtos = int(
        dados[
            "quantidade_produtos"
        ]
    )

    baixo_estoque = int(
        dados[
            "baixo_estoque"
        ]
    )

    sem_estoque = int(
        dados[
            "sem_estoque"
        ]
    )

    quantidade_compras = int(
        dados[
            "compras"
        ]
    )

    valor_comprado = dados[
        "valor_comprado"
    ]

    ticket_medio = dados[
        "ticket_medio"
    ]

    fornecedores = int(
        dados[
            "fornecedores"
        ]
    )

    criticos = normalizarProdutosCriticos(
        dados[
            "lista_baixo"
        ],

        dados[
            "lista_sem"
        ],
    )

    mais_usados = normalizarProdutosMaisUsados(
        dados[
            "mais_usados"
        ]
    )

    movimentos_tipo = normalizarMovimentacoesTipo(
        dados[
            "movimentacoes_tipo"
        ]
    )

    movimentos_recentes = normalizarMovimentacoesRecentes(
        dados[
            "movimentacoes_recentes"
        ]
    )

    mais_comprados = normalizarProdutosComprados(
        dados[
            "mais_comprados"
        ]
    )

    fornecedores_usados = normalizarFornecedores(
        dados[
            "fornecedores_usados"
        ]
    )

    renderizarMetricasDashboard(
        [
            MetricaDashboard(
                "Tipos de produtos",

                formatarInteiro(
                    tipos_produtos
                ),

                (
                    "Tipos distintos de produtos "
                    "cadastrados na rede."
                ),

                COR_ESTOQUE,

                "TP",
            ),

            MetricaDashboard(
                "Unidades em estoque",

                formatarInteiro(
                    quantidade_produtos
                ),

                (
                    "Quantidade total de unidades "
                    "disponíveis em estoque."
                ),

                "#6f8fd3",

                "UE",
            ),

            MetricaDashboard(
                "Baixo estoque",

                formatarInteiro(
                    baixo_estoque
                ),

                (
                    "Produtos abaixo da quantidade "
                    "mínima definida."
                ),

                COR_BAIXO,

                "BE",
            ),

            MetricaDashboard(
                "Sem estoque",

                formatarInteiro(
                    sem_estoque
                ),

                (
                    "Produtos atualmente sem "
                    "unidades disponíveis."
                ),

                COR_SEM_ESTOQUE,

                "SE",
            ),
        ],

        colunas=4,
    )

    secao_estoque = criarSecaoDashboard(
        titulo="Controle de estoque",

        descricao=(
            "Produtos que exigem reposição "
            "e produtos mais usados."
        ),

        meta=(
            f"{formatarInteiro(baixo_estoque)} "
            "em atenção"
        ),

        contexto="REPOSIÇÃO",

        numero=1,
    )

    with secao_estoque:

        mostrou_criticos = graficoEstoque(
            baixo_estoque,
            sem_estoque,
        )

        mostrou_usados = graficoProdutosUsados(
            mais_usados
        )

        if criticos.empty:

            if (
                not mostrou_criticos
                and not mostrou_usados
            ):

                renderizarEstadoVazio(
                    "Estoque sem alertas e ainda "
                    "sem saídas de produtos registradas."
                )

            else:

                st.caption(
                    "Nenhum produto exige "
                    "reposição no momento."
                )

        else:

            rotuloGrafico(
                "Produtos que exigem reposição",
                (
                    "Itens abaixo do mínimo ou "
                    "atualmente sem estoque."
                ),
            )

            st.dataframe(
                criticos,

                hide_index=True,

                use_container_width=True,

                row_height=38,

                column_config={
                    "Produto": (
                        st.column_config
                        .TextColumn(
                            "Produto",
                            width="large",
                        )
                    ),

                    "Marca": (
                        st.column_config
                        .TextColumn(
                            "Marca",
                        )
                    ),

                    "Quantidade": (
                        st.column_config
                        .NumberColumn(
                            "Quantidade",
                            format="%d",
                        )
                    ),

                    "Mínimo": (
                        st.column_config
                        .NumberColumn(
                            "Mínimo",
                            format="%d",
                        )
                    ),

                    "Situação": (
                        st.column_config
                        .TextColumn(
                            "Situação",
                        )
                    ),
                },
            )

    total_movimentacoes = (
        int(
            movimentos_tipo[
                "Movimentações"
            ].sum()
        )
        if not movimentos_tipo.empty
        else 0
    )

    total_unidades = (
        int(
            movimentos_tipo[
                "Unidades"
            ].sum()
        )
        if not movimentos_tipo.empty
        else 0
    )

    secao_movimentacoes = criarSecaoDashboard(
        titulo="Movimentações de estoque",

        descricao=(
            "Entradas, saídas, ajustes e "
            "perdas registradas na operação."
        ),

        meta=(
            f"{formatarInteiro(total_movimentacoes)} "
            "movimentações"
        ),

        contexto="FLUXO OPERACIONAL",

        numero=2,
    )

    with secao_movimentacoes:

        renderizarMetricasDashboard(
            [
                MetricaDashboard(
                    "Movimentações",

                    formatarInteiro(
                        total_movimentacoes
                    ),

                    (
                        "Quantidade total de registros "
                        "de movimentação."
                    ),

                    COR_COMPRA,

                    "MV",
                ),

                MetricaDashboard(
                    "Unidades movimentadas",

                    formatarInteiro(
                        total_unidades
                    ),

                    (
                        "Total de unidades envolvidas "
                        "nas movimentações."
                    ),

                    COR_ESTOQUE,

                    "UM",
                ),
            ],

            colunas=2,
        )

        mostrou_tipo = graficoMovimentacoesTipo(
            movimentos_tipo
        )

        mostrouperiodo = graficoMovimentacoesRecentes(
            movimentos_recentes
        )

        if (
            not mostrou_tipo
            and not mostrouperiodo
        ):

            renderizarEstadoVazio(
                "Ainda não existem movimentações "
                "de estoque registradas."
            )

    secao_compras = criarSecaoDashboard(
        titulo="Compras e fornecedores",

        descricao=(
            "Volume de compras realizadas e "
            "fornecedores com maior participação "
            "no abastecimento."
        ),

        meta="Rede Universitas",

        contexto="ABASTECIMENTO",

        numero=3,
    )

    with secao_compras:

        renderizarMetricasDashboard(
            [
                MetricaDashboard(
                    "Compras realizadas",

                    formatarInteiro(
                        quantidade_compras
                    ),

                    (
                        "Quantidade total de "
                        "compras registradas."
                    ),

                    COR_COMPRA,

                    "CR",
                ),

                MetricaDashboard(
                    "Valor total comprado",

                    formatarMoeda(
                        valor_comprado
                    ),

                    (
                        "Valor total gasto "
                        "nas compras."
                    ),

                    CORvalor,

                    "VT",
                ),

                MetricaDashboard(
                    "Ticket médio",

                    formatarMoeda(
                        ticket_medio
                    ),

                    (
                        "Valor médio por "
                        "compra realizada."
                    ),

                    COR_BAIXO,

                    "TM",
                ),

                MetricaDashboard(
                    "Fornecedores",

                    formatarInteiro(
                        fornecedores
                    ),

                    (
                        "Fornecedores atualmente "
                        "cadastrados."
                    ),

                    COR_FORNECEDOR,

                    "FO",
                ),
            ],

            colunas=4,
        )

        maior_produto = (
            float(
                mais_comprados["Valor gasto"]
                .apply(paraNumero)
                .max()
            )
            if not mais_comprados.empty
            else 0
        )

        maior_fornecedor = (
            float(
                fornecedores_usados["Valor gasto"]
                .apply(paraNumero)
                .max()
            )
            if not fornecedores_usados.empty
            else 0
        )

        limite_compras = max(
            maior_produto,
            maior_fornecedor,
        )

        if limite_compras > 0:
            limite_compras *= 1.05

        graficoProdutosComprados(
            mais_comprados, 
            limite_grafico=limite_compras
        )

        graficoFornecedores(
            fornecedores_usados,
            limite_grafico=limite_compras
        )