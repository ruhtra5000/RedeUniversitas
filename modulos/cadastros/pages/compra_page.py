from datetime import date
from decimal import Decimal
import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from database.entidades.Compra import Compra
from modulos.cadastros.compra import criarCompra
from modulos.compras.compras_service import listarFornecedores
from modulos.estoque.estoque_service import listarProdutos
from modulos.financeiro.financeiro_service import listarFinanceiro
from modulos.utils.cadastro_visual import (painelCadastro, renderizarAvisoCadastro, renderizarBotaoCadastro, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro)

# Tela de cadastro para Compras
def telaCadastroCompra():
    if "form_key_compra" not in st.session_state:
        st.session_state.form_key_compra = 0

    # Função para voltar à página de cadastros
    def voltarCadastros():
        from modulos.rotas import cadastros_page
        st.switch_page(cadastros_page)

    renderizarTopoCadastro(
        titulo="Registrar compra",
        descricao=(
            "Registre a aquisição de produtos e os responsáveis "
            "pela operação."
        ),
        aoVoltar=voltarCadastros,
        prefixoChave="cadastro_compra",
    )

    if st.session_state.pop("cadastro_compra_realizado", False):
        st.toast(
            "Compra registrada com sucesso!",
            icon=":material/check:",
        )

    if "cache_financeiros" not in st.session_state:
        st.session_state.cache_financeiros = listarFinanceiro()

    if "cache_fornecedores" not in st.session_state:
        st.session_state.cache_fornecedores = listarFornecedores()

    if "cache_produtos" not in st.session_state:
        st.session_state.cache_produtos = listarProdutos()

    lista_financeiros = st.session_state.cache_financeiros
    lista_fornecedores = st.session_state.cache_fornecedores
    lista_produtos = st.session_state.cache_produtos

    if not lista_financeiros or not lista_fornecedores or not lista_produtos:
        renderizarAvisoCadastro(
            titulo="Cadastros necessários",
            descricao=(
                "É necessário possuir ao menos um funcionário financeiro, "
                "um fornecedor e um produto."
            ),
        )

    with painelCadastro(
        titulo="Informações da compra",
        descricao=(
            "Defina os participantes, o produto, os valores "
            "e as datas da operação."
        ),
    ):

        renderizarSecaoCadastro(
            numero=1,
            titulo="Participantes",
            descricao="Responsável financeiro e fornecedor da compra.",
        )

        colFinanceiro, colFornecedor = st.columns(2)

        with colFinanceiro:
            financeiro_selecionado = st.selectbox(
                "Responsável financeiro *",
                options=(
                    lista_financeiros
                    if lista_financeiros
                    else []
                ),
                format_func=lambda item: item.pessoa.nome,
                index=None,
                placeholder="Selecione um funcionário...",
                disabled=not lista_financeiros,
                key=(
                    f"compra_fin_"
                    f"{st.session_state.form_key_compra}"
                ),
            )

        with colFornecedor:
            fornecedor_selecionado = st.selectbox(
                "Fornecedor *",
                options=(
                    lista_fornecedores
                    if lista_fornecedores
                    else []
                ),
                format_func=lambda item: item.nome,
                index=None,
                placeholder="Selecione um fornecedor...",
                disabled=not lista_fornecedores,
                key=(
                    f"compra_forn_"
                    f"{st.session_state.form_key_compra}"
                ),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Produto",
            descricao="Item adquirido e quantidade solicitada.",
        )

        colProduto, colQuantidade = st.columns([3, 1])

        with colProduto:
            produto_selecionado = st.selectbox(
                "Produto (estoque) *",
                options=lista_produtos if lista_produtos else [],
                format_func=(
                    lambda item: (
                        f"{item.nome} ({item.campus.nome})"
                    )
                ),
                index=None,
                placeholder="Selecione o produto...",
                disabled=not lista_produtos,
                key=(
                    f"compra_prod_"
                    f"{st.session_state.form_key_compra}"
                ),
            )

        with colQuantidade:
            qtde = st.number_input(
                "Quantidade *",
                min_value=1,
                step=1,
                key=(
                    f"compra_qtde_"
                    f"{st.session_state.form_key_compra}"
                ),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=3,
            titulo="Valores e datas",
            descricao="Valor unitário, emissão e vencimento da compra.",
        )

        colValor, colCompra, colVencimento = st.columns(3)

        with colValor:
            valor_unit = st.number_input(
                "Valor unitário (R$) *",
                min_value=0.01,
                step=10.0,
                format="%.2f",
                key=(
                    f"compra_vunit_"
                    f"{st.session_state.form_key_compra}"
                ),
            )

        with colCompra:
            data_compra = st.date_input(
                "Data da compra *",
                format="DD/MM/YYYY",
                key=(
                    f"compra_dcompra_"
                    f"{st.session_state.form_key_compra}"
                ),
            )

        with colVencimento:
            data_vencimento = st.date_input(
                "Vencimento da parcela *",
                format="DD/MM/YYYY",
                key=(
                    f"compra_venc_"
                    f"{st.session_state.form_key_compra}"
                ),
            )

        cadastrar = renderizarBotaoCadastro(
            rotulo="Registrar compra",
            icone=":material/add_shopping_cart:",
            chave=(
                f"btn_cad_compra_"
                f"{st.session_state.form_key_compra}"
            ),
        )

    if cadastrar:
        if not lista_financeiros or not lista_fornecedores or not lista_produtos:
            st.error("Cadastre os requisitos básicos antes de continuar.")

        elif financeiro_selecionado is None:
            st.error("Por favor, selecione um Responsável Financeiro.")

        elif fornecedor_selecionado is None:
            st.error("Por favor, selecione um Fornecedor.")

        elif produto_selecionado is None:
            st.error("Por favor, selecione um Produto.")

        else:
            try:
                nova_compra = Compra(
                    produto_id=produto_selecionado.id,
                    qtde=qtde,
                    valor_unit=Decimal(str(valor_unit)),
                    data_compra=data_compra,
                    financeiro_id=financeiro_selecionado.pessoa_id,
                    fornecedor_id=fornecedor_selecionado.id,
                    data_recebimento=None,
                )

                criarCompra(
                    compra=nova_compra,
                    dataVencimentoContaPagar=data_vencimento,
                    financeiro=financeiro_selecionado,
                )

                st.session_state.form_key_compra += 1
                st.session_state["cadastro_compra_realizado"] = True

                st.rerun()

            except SQLAlchemyError as erro:
                st.error(
                    "Erro ao salvar os dados no banco: "
                    f"{erro}"
                )

            except Exception as erro:
                st.error(
                    "Houve um erro interno ao tentar registrar "
                    f"uma compra: {erro}"
                )
