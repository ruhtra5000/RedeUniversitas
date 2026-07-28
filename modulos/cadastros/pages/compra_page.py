from datetime import date
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from database.Conexao import SessionLocal
from database.entidades.Compra import Compra
from modulos.cadastros.compra import criarCompra
from modulos.financeiro.financeiro_service import listarFinanceiro
from modulos.compras.compras_service import listarFornecedores
from modulos.estoque.estoque_service import listarProdutosGeral
import database.entidades

def telaCadastroCompra():
    if "form_key_compra" not in st.session_state:
        st.session_state.form_key_compra = 0

    st.title("🛒 Registro de Compra")
    st.caption("Preencha as informações abaixo para registrar uma compra de produtos.")

    st.markdown(
        """
        <style>
        div[data-testid="InputInstructions"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.pop("cadastro_compra_realizado", False):
        st.toast("Compra registrada com sucesso!", icon=":material/check:")

    col1, _ = st.columns([1, 6])
    with col1:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import cadastros_page
            st.switch_page(cadastros_page)

    if "cache_financeiros" not in st.session_state:
        st.session_state.cache_financeiros = listarFinanceiro()

    if "cache_fornecedores" not in st.session_state:
        st.session_state.cache_fornecedores = listarFornecedores()
        
    if "cache_produtos" not in st.session_state:
        st.session_state.cache_produtos = listarProdutosGeral()

    lista_financeiros = st.session_state.cache_financeiros
    lista_fornecedores = st.session_state.cache_fornecedores
    lista_produtos = st.session_state.cache_produtos

    if not lista_financeiros or not lista_fornecedores or not lista_produtos:
        st.warning(
            """
            ⚠️ Antes de registrar uma compra é necessário possuir:
            - Pelo menos **1 Funcionário Financeiro**
            - Pelo menos **1 Fornecedor**
            - Pelo menos **1 Produto (Estoque)**
            """
        )

    with st.form(key=f"cadastro_compra_{st.session_state.form_key_compra}", border=False):
        
        with st.container(border=True):
            st.subheader("🛒 Informações da Compra")
            
            with st.container(horizontal=True):
                financeiro_selecionado = st.selectbox(
                    "Responsável Financeiro *",
                    options=lista_financeiros if lista_financeiros else [],
                    format_func=lambda f: f.pessoa.nome,
                    index=None,
                    placeholder="Selecione um funcionário...",
                    disabled=not lista_financeiros,
                    key=f"compra_fin_{st.session_state.form_key_compra}"
                )
                fornecedor_selecionado = st.selectbox(
                    "Fornecedor *",
                    options=lista_fornecedores if lista_fornecedores else [],
                    format_func=lambda f: f.nome,
                    index=None,
                    placeholder="Selecione um fornecedor...",
                    disabled=not lista_fornecedores,
                    key=f"compra_forn_{st.session_state.form_key_compra}"
                )

            with st.container(horizontal=True):
                produto_selecionado = st.selectbox(
                    "Produto (Estoque) *",
                    options=lista_produtos if lista_produtos else [],
                    format_func=lambda p: f"{p.nome} ({p.campus.nome})",
                    index=None,
                    placeholder="Selecione o produto...",
                    disabled=not lista_produtos,
                    key=f"compra_prod_{st.session_state.form_key_compra}"
                )
                qtde = st.number_input(
                    "Quantidade *",
                    min_value=1,
                    step=1,
                    key=f"compra_qtde_{st.session_state.form_key_compra}"
                )

        st.write("")

        with st.container(border=True):
            st.subheader("💰 Valores e Datas")

            with st.container(horizontal=True):
                valor_unit = st.number_input(
                    "Valor Unitário (R$) *",
                    min_value=0.01,
                    step=10.0,
                    format="%.2f",
                    key=f"compra_vunit_{st.session_state.form_key_compra}"
                )
                data_compra = st.date_input(
                    "Data da Compra *",
                    format="DD/MM/YYYY",
                    key=f"compra_dcompra_{st.session_state.form_key_compra}"
                )

        st.write("")

        with st.container(border=True):
            st.subheader("💳 Condições de Pagamento")

            with st.container(horizontal=True):
                data_vencimento = st.date_input(
                    "Data de Vencimento da Parcela *",
                    format="DD/MM/YYYY",
                    key=f"compra_venc_{st.session_state.form_key_compra}"
                )

        st.write("")

        _, centro, _ = st.columns([2, 3, 2])
        with centro:
            cadastrar = st.form_submit_button(
                "💾 Registrar Compra", 
                type="primary", 
                use_container_width=True
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
                    data_recebimento=None
                )
                
                criarCompra(
                    compra=nova_compra,
                    dataVencimentoContaPagar=data_vencimento,
                    financeiro=financeiro_selecionado
                )
                
                st.session_state.form_key_compra += 1
                st.session_state["cadastro_compra_realizado"] = True
                
                st.rerun()
                
            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(f"Houve um erro interno ao tentar registrar uma compra: {str(e)}")