from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from validate_docbr.CPF import CPF
from database.Conexao import SessionLocal
from database.entidades.Pessoa import Pessoa
from database.entidades.Professor import Professor
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
from modulos.academico.academico_service import listarCampus
from modulos.cadastros.professor import criarProfessor

import database.entidades

def telaCadastroProfessor():

    if "form_key_prof" not in st.session_state:
        st.session_state.form_key_prof = 0

    st.title("👨‍🏫 Cadastro de Professor")
    st.caption("Preencha as informações abaixo para cadastrar um novo professor.")
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

    if st.session_state.pop("cadastro_prof_realizado", False):
        st.toast("Professor cadastrado com sucesso!", icon=":material/check:")

    col1, _ = st.columns([1, 6])

    with col1:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import cadastros_page # evita import circular
            st.switch_page(cadastros_page)

    if "cache_campus" not in st.session_state:
        st.session_state.cache_campus = listarCampus()

    lista_campus = st.session_state.cache_campus

    if not lista_campus:
        st.warning(
            """
            ⚠️ Antes de cadastrar um professor é necessário possuir:

            - Pelo menos **1 Campus**
            """
        )

    with st.form(key=f"cadastro_prof_{st.session_state.form_key_prof}", border=False):

        # Dados Pessoais
        with st.container(border=True):
            st.subheader("👤 Dados Pessoais")
            
            with st.container(horizontal=True):
                nome = st.text_input(
                    "Nome Completo *",
                    placeholder="Ex.: Carlos Mendes",
                    key=f"prof_nome_{st.session_state.form_key_prof}"
                )
                email = st.text_input(
                    "E-mail *",
                    placeholder="email@exemplo.com",
                    key=f"prof_email_{st.session_state.form_key_prof}"
                )

            with st.container(horizontal=True):
                cpf = st.text_input(
                    "CPF *",
                    placeholder="Somente números",
                    key=f"prof_cpf_{st.session_state.form_key_prof}"
                )
                telefone = st.text_input(
                    "Telefone",
                    placeholder="Opcional",
                    key=f"prof_telefone_{st.session_state.form_key_prof}"
                )

        st.write("")

        # Vínculo Institucional
        with st.container(border=True):
            st.subheader("🔗 Vínculo Institucional")

            campus = st.selectbox(
                "Campus *",
                options=lista_campus if lista_campus else [],
                format_func=lambda x: x.nome,
                index=None,
                placeholder="Selecione um campus...",
                disabled=not lista_campus,
                key=f"prof_campus_{st.session_state.form_key_prof}"
            )

        st.write("")

        _, centro, _ = st.columns([2, 3, 2])
        
        with centro:
            cadastrar = st.form_submit_button(
                "💾 Cadastrar Professor", 
                type="primary", 
                use_container_width=True
            )

    # Processamento
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
                
                criarProfessor(pessoa=nova_pessoa, idCampus=campus.id)
                
                st.session_state.form_key_prof += 1 
                st.session_state["cadastro_prof_realizado"] = True
                st.session_state.pop("cache_professores", None)
                st.rerun()
                
            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(str(e))