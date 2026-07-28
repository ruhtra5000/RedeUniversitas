from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from database.Conexao import SessionLocal
from database.entidades.Pessoa import Pessoa
from database.entidades.Financeiro import Financeiro
from modulos.cadastros.financeiro import criarFinanceiro
from modulos.academico.academico_service import listarCampus
import database.entidades

def telaCadastroFinanceiro():
    if "form_key_fin" not in st.session_state:
        st.session_state.form_key_fin = 0

    col1, _ = st.columns([1, 6])
    with col1:
        if st.button(":material/arrow_back: Voltar", width="stretch"):
            from modulos.rotas import cadastros_page
            st.switch_page(cadastros_page)

    st.title(":material/person_add: Cadastro de Financeiro")
    st.caption("Preencha as informações abaixo para cadastrar um novo funcionário financeiro no sistema.")

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

    if st.session_state.pop("cadastro_fin_realizado", False):
        st.toast("Funcionário financeiro cadastrado com sucesso!", icon=":material/check:")

    if "cache_campus" not in st.session_state:
        st.session_state.cache_campus = listarCampus()

    lista_campus = st.session_state.cache_campus

    if not lista_campus:
        st.warning(
            """
            :material/warning: Antes de cadastrar um funcionário financeiro é necessário possuir:
            - Pelo menos **1 Campus**
            """
        )

    with st.form(key=f"cadastro_fin_{st.session_state.form_key_fin}", border=False):
        
        with st.container():
            st.subheader("Dados Pessoais")
            
            with st.container(horizontal=True):
                nome = st.text_input(
                    "Nome Completo *",
                    placeholder="Ex.: Carlos Mendes",
                    key=f"fin_nome_{st.session_state.form_key_fin}"
                )
                email = st.text_input(
                    "E-mail *",
                    placeholder="email@exemplo.com",
                    key=f"fin_email_{st.session_state.form_key_fin}"
                )

            with st.container(horizontal=True):
                cpf = st.text_input(
                    "CPF *",
                    placeholder="Somente números",
                    key=f"fin_cpf_{st.session_state.form_key_fin}"
                )
                telefone = st.text_input(
                    "Telefone",
                    placeholder="Opcional",
                    key=f"fin_telefone_{st.session_state.form_key_fin}"
                )


        with st.container():
            st.subheader("Vínculo Institucional")

            campus = st.selectbox(
                "Campus *",
                options=lista_campus if lista_campus else [],
                format_func=lambda x: x.nome,
                index=None,
                placeholder="Selecione um campus...",
                disabled=not lista_campus,
                key=f"fin_campus_{st.session_state.form_key_fin}"
            )

        st.write("")

        _, centro, _ = st.columns([2, 3, 2])
        with centro:
            cadastrar = st.form_submit_button(
                "Cadastrar Financeiro", 
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
                
                criarFinanceiro(pessoa=nova_pessoa, idCampus=campus.id)
                
                st.session_state.form_key_fin += 1 
                st.session_state["cadastro_fin_realizado"] = True
                
                st.rerun()
                
            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(str(e))