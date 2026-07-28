from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from database.entidades.Estoque import Estoque
from modulos.cadastros.estoque import criarEstoque
from modulos.academico.academico_service import listarCampus
import database.entidades

def telaCadastroEstoque():
    if "form_key_estoque" not in st.session_state:
        st.session_state.form_key_estoque = 0

    col1, _ = st.columns([1, 6])
    with col1:
        if st.button(":material/arrow_back: Voltar", width="stretch"):
            from modulos.rotas import cadastros_page
            st.switch_page(cadastros_page)

    st.title(":material/inventory_2: Cadastro de Produto")
    st.caption("Preencha as informações abaixo para cadastrar um novo produto no estoque do campus.")

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

    if st.session_state.pop("cadastro_estoque_realizado", False):
        st.toast("Produto cadastrado com sucesso!", icon=":material/check:")

    if "cache_campus" not in st.session_state:
        st.session_state.cache_campus = listarCampus()

    lista_campus = st.session_state.cache_campus

    if not lista_campus:
        st.warning(":material/warning: Antes de cadastrar um produto, é necessário cadastrar pelo menos 1 Campus.")

    with st.form(key=f"cadastro_estoque_{st.session_state.form_key_estoque}", border=False):
        with st.container():
            st.subheader("Dados do Produto")
            
            with st.container(horizontal=True):
                nome = st.text_input(
                    "Nome do Produto *",
                    placeholder="Ex.: Resma de Papel A4",
                    key=f"est_nome_{st.session_state.form_key_estoque}"
                )
                marca = st.text_input(
                    "Marca *",
                    placeholder="Ex.: Chamex",
                    key=f"est_marca_{st.session_state.form_key_estoque}"
                )

            with st.container(horizontal=True):
                campus_selecionado = st.selectbox(
                    "Campus de Alocação *",
                    options=lista_campus if lista_campus else [],
                    format_func=lambda c: c.nome,
                    index=None,
                    placeholder="Selecione um campus...",
                    disabled=not lista_campus,
                    key=f"est_campus_{st.session_state.form_key_estoque}"
                )
            with st.container(horizontal=True):
                qtde = st.number_input(
                    "Quantidade Atual",
                    min_value=0,
                    value=0,
                    step=1,
                    help="Quantidade do produto que já se encontra em estoque, se houver.",
                    key=f"est_qtde_{st.session_state.form_key_estoque}"
                )
                qtde_min = st.number_input(
                    "Quantidade Mínima *",
                    min_value=0,
                    value=0,
                    step=1,
                    help="Quantidade mínima recomendada para acionar um alerta de reposição.",
                    key=f"est_qtde_min_{st.session_state.form_key_estoque}"
                )

        st.write("")
        
        _, centro, _ = st.columns([2, 3, 2])
        with centro:
            cadastrar = st.form_submit_button(
                "Cadastrar Produto", 
                type="primary", 
                width="stretch"
            )

    if cadastrar:
        if not lista_campus:
            st.error("Cadastre pelo menos um Campus antes de continuar.")
        elif not nome.strip() or not marca.strip():
            st.error("Por favor, preencha os campos obrigatórios (Nome e Marca).")
        elif campus_selecionado is None:
            st.error("Por favor, selecione um Campus.")
        else:
            try:
                novo_produto = Estoque(
                    nome=nome.strip(),
                    marca=marca.strip(),
                    qtde=qtde,
                    qtde_min=qtde_min,
                    campus_id=campus_selecionado.id
                )
                
                criarEstoque(produto=novo_produto)
                
                st.session_state.form_key_estoque += 1 
                st.session_state.pop("cache_produtos", None) 
                st.session_state["cadastro_estoque_realizado"] = True
                
                st.rerun()
                
            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(str(e))
