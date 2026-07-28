from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from database.Conexao import SessionLocal
from database.entidades.Pessoa import Pessoa
from database.entidades.Almoxarife import Almoxarife
from modulos.cadastros.almoxarife import criarAlmoxarife
from modulos.academico.academico_service import listarCampus
import database.entidades

def telaCadastroAlmoxarife():
    if "form_key_alm" not in st.session_state:
        st.session_state.form_key_alm = 0

    st.title("📦 Cadastro de Almoxarife")
    st.caption("Preencha as informações abaixo para cadastrar um novo almoxarife no sistema.")

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

    if st.session_state.pop("cadastro_alm_realizado", False):
        st.toast("Almoxarife cadastrado com sucesso!", icon=":material/check:")

    col1, _ = st.columns([1, 6])
    with col1:
        if st.button("⬅ Voltar", width="stretch"):
            from modulos.rotas import cadastros_page
            st.switch_page(cadastros_page)

    if "cache_campus" not in st.session_state:
        st.session_state.cache_campus = listarCampus()

    lista_campus = st.session_state.cache_campus

    if not lista_campus:
        st.warning(
            """
            ⚠️ Antes de cadastrar um almoxarife é necessário possuir:
            - Pelo menos **1 Campus**
            """
        )

    with st.form(key=f"cadastro_alm_{st.session_state.form_key_alm}", border=False):
        
        with st.container(border=True):
            st.subheader("👤 Dados Pessoais")
            
            with st.container(horizontal=True):
                nome = st.text_input(
                    "Nome Completo *",
                    placeholder="Ex.: Maria Oliveira",
                    key=f"alm_nome_{st.session_state.form_key_alm}"
                )
                email = st.text_input(
                    "E-mail *",
                    placeholder="email@exemplo.com",
                    key=f"alm_email_{st.session_state.form_key_alm}"
                )

            with st.container(horizontal=True):
                cpf = st.text_input(
                    "CPF *",
                    placeholder="Somente números",
                    key=f"alm_cpf_{st.session_state.form_key_alm}"
                )
                telefone = st.text_input(
                    "Telefone",
                    placeholder="Opcional",
                    key=f"alm_telefone_{st.session_state.form_key_alm}"
                )

        st.write("")

        with st.container(border=True):
            st.subheader("🔗 Vínculo Institucional")

            campus = st.selectbox(
                "Campus *",
                options=lista_campus if lista_campus else [],
                format_func=lambda x: x.nome,
                index=None,
                placeholder="Selecione um campus...",
                disabled=not lista_campus,
                key=f"alm_campus_{st.session_state.form_key_alm}"
            )

        st.write("")

        _, centro, _ = st.columns([2, 3, 2])
        with centro:
            cadastrar = st.form_submit_button(
                "💾 Cadastrar Almoxarife", 
                type="primary", 
                width="stretch"
            )

    if cadastrar:
        if not lista_campus:
            st.error("Cadastre pelo menos um Campus antes de continuar.")
        elif not nome.strip() or not cpf.strip() or not email.strip():
            st.error("Por favor, preencha todos os campos obrigatórios.")
        elif campus is None:
            st.error("Por favor, selecione um Campus.")
        else:
            try:
                import re
                nova_pessoa = Pessoa(
                    nome=nome.strip(),
                    cpf=re.sub(r'\D', '', cpf),
                    email=email.strip(),
                    telefone=telefone.strip() if telefone.strip() != "" else None
                )
                
                criarAlmoxarife(pessoa=nova_pessoa, idCampus=campus.id)
                
                st.session_state.form_key_alm += 1 
                st.session_state["cadastro_alm_realizado"] = True
                
                st.rerun()
                
            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(str(e))
