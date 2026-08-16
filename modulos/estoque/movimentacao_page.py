import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from database.entidades.enums.StatusMovimentacao import (StatusMovimentacao)
from modulos.estoque.estoque_service import (criarMovimentacao, listarAlmoxarifes, listarProdutos)
from modulos.utils.cadastro_visual import (painelCadastro, renderizarAvisoCadastro, renderizarBotaoCadastro, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro)

# Rotulos dos tipos de movimentação para exibição na interface do usuário
ROTULOS_MOVIMENTACAO = {
    StatusMovimentacao.ENTRADA: "Entrada",
    StatusMovimentacao.SAIDA: "Saída",
    StatusMovimentacao.AJUSTE: "Ajuste de estoque",
    StatusMovimentacao.PERDA: "Perda",
}

# Função principal da tela de movimentação de estoque
def telaMovimentacaoEstoque():

    if "form_key_movimentacao" not in st.session_state:
        st.session_state.form_key_movimentacao = 0

    # Função para voltar à página inicial
    def voltar():
        from modulos.rotas import home_page

        st.switch_page(home_page)

    renderizarTopoCadastro(
        titulo="Movimentação de estoque",
        descricao=(
            "Registre entradas, saídas, perdas e ajustes "
            "dos produtos armazenados."
        ),
        aoVoltar=voltar,
        prefixoChave="movimentacao_estoque",
        categoria="ESTOQUE",
    )

    if st.session_state.pop(
        "movimentacao_realizada",
        False,
    ):
        st.toast(
            "Movimentação registrada com sucesso!",
            icon=":material/check:",
        )

    try:
        listaAlmoxarifes = listarAlmoxarifes()
        listaProdutos = listarProdutos()

    except Exception as erro:
        st.error(
            "Não foi possível carregar os dados necessários."
        )
        st.caption(
            f"Detalhes técnicos: {erro}"
        )
        return

    if not listaAlmoxarifes:
        renderizarAvisoCadastro(
            titulo="Almoxarife necessário",
            descricao=(
                "Cadastre pelo menos um almoxarife antes "
                "de registrar uma movimentação."
            ),
        )

    if not listaProdutos:
        renderizarAvisoCadastro(
            titulo="Produto necessário",
            descricao=(
                "Cadastre pelo menos um produto antes "
                "de registrar uma movimentação."
            ),
        )

    with painelCadastro(
        titulo="Dados da movimentação",
        descricao=(
            "Selecione o responsável, o produto e informe "
            "o tipo e a quantidade da operação."
        ),
        contexto="NOVA MOVIMENTAÇÃO",
    ):

        renderizarSecaoCadastro(
            numero=1,
            titulo="Responsável",
            descricao=(
                "Almoxarife responsável pela movimentação."
            ),
        )

        almoxarifeSelecionado = st.selectbox(
            "Almoxarife responsável *",
            options=(
                listaAlmoxarifes
                if listaAlmoxarifes
                else []
            ),
            format_func=lambda almoxarife: (
                f"{almoxarife.pessoa.nome} — "
                f"{almoxarife.campus.nome}"
            ),
            index=None,
            placeholder="Selecione um almoxarife...",
            disabled=not listaAlmoxarifes,
            key=(
                f"mov_almoxarife_"
                f"{st.session_state.form_key_movimentacao}"
            ),
        )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Produto",
            descricao=(
                "Produto que terá sua quantidade em estoque alterada."
            ),
        )

        if almoxarifeSelecionado is not None:

            produtosCampus = [
                produto
                for produto in listaProdutos
                if produto.campus_id
                == almoxarifeSelecionado.campus_id
            ]

        else:
            produtosCampus = []


        colProduto, colEstoque = st.columns(
            [3, 1]
        )

        with colProduto:

            produtoSelecionado = st.selectbox(
                "Produto *",
                options=produtosCampus,
                format_func=lambda produto: (
                    f"{produto.nome}"
                    + (
                        f" — {produto.marca}"
                        if produto.marca
                        else ""
                    )
                ),
                index=None,
                placeholder=(
                    "Selecione primeiro o almoxarife..."
                    if almoxarifeSelecionado is None
                    else "Selecione um produto..."
                ),
                disabled=(
                    almoxarifeSelecionado is None
                    or not produtosCampus
                ),
                key=(
                    f"mov_produto_"
                    f"{st.session_state.form_key_movimentacao}"
                ),
            )

        with colEstoque:
            estoqueAtual = (
                int(produtoSelecionado.qtde)
                if produtoSelecionado is not None
                else 0
            )

            st.html(
                f"""
                <div style="
                    margin-top: 0;
                ">
                    <div style="
                        color: #E8EEF6;
                        font-size: 0.875rem;
                        font-weight: 500;
                        margin-bottom: 0.45rem;
                    ">
                        Estoque atual
                    </div>

                    <div style="
                        height: 42px;
                        display: flex;
                        align-items: center;
                        justify-content: space-between;

                        padding: 0 0.85rem;

                        background: rgba(15, 29, 48, 0.82);

                        border: 1px solid rgba(148, 163, 184, 0.18);
                        border-radius: 8px;

                        color: #E8EEF6;

                        font-size: 0.95rem;
                        font-weight: 700;
                    ">
                        <span>{estoqueAtual}</span>

                        <span style="
                            color: #60738A;
                            font-size: 0.68rem;
                            font-weight: 700;
                            letter-spacing: 0.05em;
                            text-transform: uppercase;
                        ">
                            unidades
                        </span>
                    </div>
                </div>
                """
            )

        if (
            almoxarifeSelecionado is not None
            and not produtosCampus
        ):
            renderizarAvisoCadastro(
                titulo="Nenhum produto disponível",
                descricao=(
                    "Não existem produtos cadastrados no mesmo "
                    "campus do almoxarife selecionado."
                ),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=3,
            titulo="Operação",
            descricao=(
                "Defina o tipo da movimentação e a quantidade."
            ),
        )

        colTipo, colQuantidade = st.columns(2)

        with colTipo:

            tipoSelecionado = st.selectbox(
                "Tipo de movimentação *",
                options=list(
                    StatusMovimentacao
                ),
                format_func=lambda tipo: (
                    ROTULOS_MOVIMENTACAO[tipo]
                ),
                index=None,
                placeholder=(
                    "Selecione o tipo..."
                ),
                key=(
                    f"mov_tipo_"
                    f"{st.session_state.form_key_movimentacao}"
                ),
            )

        if (
            tipoSelecionado
            == StatusMovimentacao.AJUSTE
        ):
            rotuloQuantidade = (
                "Novo saldo do estoque *"
            )

            ajudaQuantidade = (
                "Informe a quantidade física correta "
                "existente no estoque."
            )

        elif (
            tipoSelecionado
            == StatusMovimentacao.ENTRADA
        ):
            rotuloQuantidade = (
                "Quantidade de entrada *"
            )

            ajudaQuantidade = (
                "Quantidade que será adicionada "
                "ao estoque atual."
            )

        elif (
            tipoSelecionado
            == StatusMovimentacao.SAIDA
        ):
            rotuloQuantidade = (
                "Quantidade de saída *"
            )

            ajudaQuantidade = (
                "Quantidade que será retirada "
                "do estoque atual."
            )

        elif (
            tipoSelecionado
            == StatusMovimentacao.PERDA
        ):
            rotuloQuantidade = (
                "Quantidade perdida *"
            )

            ajudaQuantidade = (
                "Quantidade que será removida "
                "do estoque devido à perda."
            )

        else:
            rotuloQuantidade = "Quantidade *"

            ajudaQuantidade = (
                "Informe a quantidade da movimentação."
            )

        with colQuantidade:

            quantidade = st.number_input(
                rotuloQuantidade,
                min_value=1,
                value=1,
                step=1,
                help=ajudaQuantidade,
                key=(
                    f"mov_quantidade_"
                    f"{st.session_state.form_key_movimentacao}"
                ),
            )

        if (
            produtoSelecionado is not None
            and tipoSelecionado is not None
        ):

            estoqueAtual = int(
                produtoSelecionado.qtde
            )

            if (
                tipoSelecionado
                == StatusMovimentacao.ENTRADA
            ):

                estoquePosterior = (
                    estoqueAtual
                    + quantidade
                )

            elif (
                tipoSelecionado
                in (
                    StatusMovimentacao.SAIDA,
                    StatusMovimentacao.PERDA,
                )
            ):

                estoquePosterior = (
                    estoqueAtual
                    - quantidade
                )

            else:
                estoquePosterior = (
                    quantidade
                )

            renderizarDivisorCadastro()

            renderizarSecaoCadastro(
                numero=4,
                titulo="Prévia",
                descricao=(
                    "Confira o impacto da movimentação "
                    "antes de confirmar."
                ),
            )

            if tipoSelecionado == StatusMovimentacao.ENTRADA:
                textoOperacao = f"+{quantidade}"
                corOperacao = "#54b68a"

            elif tipoSelecionado == StatusMovimentacao.SAIDA:
                textoOperacao = f"-{quantidade}"
                corOperacao = "#6f8fd3"

            elif tipoSelecionado == StatusMovimentacao.PERDA:
                textoOperacao = f"-{quantidade}"
                corOperacao = "#cf6871"

            else:
                textoOperacao = f"→ {quantidade}"
                corOperacao = "#d4a84f"

            colAntes, colOperacao, colDepois = st.columns(
                3,
                gap="medium",
            )

            with colAntes:
                st.html(
                    f"""
                    <div style="
                        padding: 0.85rem 1rem;
                        background: rgba(15, 29, 48, 0.82);
                        border: 1px solid rgba(148, 163, 184, 0.16);
                        border-radius: 10px;
                        min-height: 88px;
                    ">
                        <div style="
                            color: #8190A4;
                            font-size: 0.65rem;
                            font-weight: 800;
                            letter-spacing: 0.06em;
                            text-transform: uppercase;
                            margin-bottom: 0.45rem;
                        ">
                            Estoque atual
                        </div>

                        <div style="
                            color: #F4F7FB;
                            font-size: 1.55rem;
                            font-weight: 800;
                            line-height: 1;
                        ">
                            {estoqueAtual}
                        </div>

                        <div style="
                            color: #60738A;
                            font-size: 0.68rem;
                            margin-top: 0.45rem;
                        ">
                            unidades disponíveis
                        </div>
                    </div>
                    """
                )

            with colOperacao:
                st.html(
                    f"""
                    <div style="
                        padding: 0.85rem 1rem;
                        background: rgba(15, 29, 48, 0.82);
                        border: 1px solid rgba(148, 163, 184, 0.16);
                        border-radius: 10px;
                        min-height: 88px;
                    ">
                        <div style="
                            color: #8190A4;
                            font-size: 0.65rem;
                            font-weight: 800;
                            letter-spacing: 0.06em;
                            text-transform: uppercase;
                            margin-bottom: 0.45rem;
                        ">
                            {ROTULOS_MOVIMENTACAO[tipoSelecionado]}
                        </div>

                        <div style="
                            color: {corOperacao};
                            font-size: 1.55rem;
                            font-weight: 800;
                            line-height: 1;
                        ">
                            {textoOperacao}
                        </div>

                        <div style="
                            color: #60738A;
                            font-size: 0.68rem;
                            margin-top: 0.45rem;
                        ">
                            impacto da operação
                        </div>
                    </div>
                    """
                )

            with colDepois:
                corSaldo = (
                    "#cf6871"
                    if estoquePosterior < 0
                    else "#54b68a"
                )

                st.html(
                    f"""
                    <div style="
                        padding: 0.85rem 1rem;
                        background: rgba(15, 29, 48, 0.82);
                        border: 1px solid rgba(148, 163, 184, 0.16);
                        border-radius: 10px;
                        min-height: 88px;
                    ">
                        <div style="
                            color: #8190A4;
                            font-size: 0.65rem;
                            font-weight: 800;
                            letter-spacing: 0.06em;
                            text-transform: uppercase;
                            margin-bottom: 0.45rem;
                        ">
                            Saldo após operação
                        </div>

                        <div style="
                            color: {corSaldo};
                            font-size: 1.55rem;
                            font-weight: 800;
                            line-height: 1;
                        ">
                            {estoquePosterior}
                        </div>

                        <div style="
                            color: #60738A;
                            font-size: 0.68rem;
                            margin-top: 0.45rem;
                        ">
                            unidades após a movimentação
                        </div>
                    </div>
                    """
                )

            if estoquePosterior < 0:
                st.error(
                    "Essa operação deixaria o estoque negativo."
                )

        registrar = renderizarBotaoCadastro(
            rotulo="Registrar movimentação",
            icone=":material/swap_vert:",
            chave=(
                f"btn_movimentacao_"
                f"{st.session_state.form_key_movimentacao}"
            ),
        )

    if registrar:

        if not listaAlmoxarifes:
            st.error(
                "Nenhum almoxarife cadastrado."
            )

        elif not listaProdutos:
            st.error(
                "Nenhum produto cadastrado."
            )

        elif almoxarifeSelecionado is None:
            st.error(
                "Selecione o almoxarife responsável."
            )

        elif produtoSelecionado is None:
            st.error(
                "Selecione um produto."
            )

        elif tipoSelecionado is None:
            st.error(
                "Selecione o tipo da movimentação."
            )

        elif quantidade <= 0:
            st.error(
                "A quantidade deve ser maior que zero."
            )

        elif (
            tipoSelecionado
            in (
                StatusMovimentacao.SAIDA,
                StatusMovimentacao.PERDA,
            )
            and quantidade
            > produtoSelecionado.qtde
        ):
            st.error(
                "A quantidade informada é maior "
                "que o estoque disponível."
            )

        else:

            try:

                criarMovimentacao(
                    idProduto=produtoSelecionado.id,
                    idAlmoxarife=(
                        almoxarifeSelecionado.pessoa_id
                    ),
                    qtde=int(
                        quantidade
                    ),
                    tipo=tipoSelecionado,
                )

                st.session_state.form_key_movimentacao += 1

                st.session_state[
                    "movimentacao_realizada"
                ] = True

                st.rerun()

            except SQLAlchemyError as erro:

                st.error(
                    "Erro ao salvar a movimentação "
                    f"no banco: {erro}"
                )

            except Exception as erro:

                st.error(
                    str(erro)
                )