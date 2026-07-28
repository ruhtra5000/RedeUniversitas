from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from database.Conexao import SessionLocal
from database.entidades.Fornecedor import Fornecedor
from modulos.cadastros.fornecedor import criarFornecedor
import database.entidades

def telaCadastroFornecedor():
    if "form_key_forn" not in st.session_state:
        st.session_state.form_key_forn = 0

    st.title("🚚 Cadastro de Fornecedor")
    st.caption("Preencha as informações abaixo para cadastrar um novo fornecedor.")

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

    if st.session_state.pop("cadastro_forn_realizado", False):
        st.toast("Fornecedor cadastrado com sucesso!", icon=":material/check:")

    col1, _ = st.columns([1, 6])
    with col1:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import cadastros_page
            st.switch_page(cadastros_page)

    with st.form(key=f"cadastro_forn_{st.session_state.form_key_forn}", border=False):
        
        with st.container(border=True):
            st.subheader("🏢 Dados da Empresa")
            
            with st.container(horizontal=True):
                nome = st.text_input(
                    "Razão Social *",
                    placeholder="Ex.: Distribuidora X",
                    key=f"forn_nome_{st.session_state.form_key_forn}"
                )
                cnpj = st.text_input(
                    "CNPJ *",
                    placeholder="Somente números",
                    key=f"forn_cnpj_{st.session_state.form_key_forn}"
                )

        st.write("")

        with st.container(border=True):
            st.subheader("📞 Contato")

            with st.container(horizontal=True):
                telefone = st.text_input(
                    "Telefone *",
                    placeholder="Ex.: 11999999999",
                    key=f"forn_telefone_{st.session_state.form_key_forn}"
                )
                email = st.text_input(
                    "E-mail *",
                    placeholder="contato@empresa.com",
                    key=f"forn_email_{st.session_state.form_key_forn}"
                )

        st.write("")

        _, centro, _ = st.columns([2, 3, 2])
        with centro:
            cadastrar = st.form_submit_button(
                "💾 Cadastrar Fornecedor", 
                type="primary", 
                use_container_width=True
            )

    if cadastrar:
        if not nome.strip() or not cnpj.strip() or not email.strip() or not telefone.strip():
            st.error("Por favor, preencha todos os campos obrigatórios.")
        else:
            try:
                import re
                novo_fornecedor = Fornecedor(
                    cnpj=re.sub(r'\D', '', cnpj),
                    nome=nome.strip(),
                    email=email.strip(),
                    telefone=telefone.strip()
                )
                
                criarFornecedor(fornecedor=novo_fornecedor)
                
                st.session_state.form_key_forn += 1
                st.session_state.pop("cache_fornecedores", None) 
                st.session_state["cadastro_forn_realizado"] = True
                
                st.rerun()
                
            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(str(e))