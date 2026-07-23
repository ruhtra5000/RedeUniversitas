from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from validate_docbr.CPF import CPF

from database.Conexao import SessionLocal
from database.entidades.Pessoa import Pessoa
from database.entidades.Professor import Professor
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
import database.entidades
from modulos.rotas import ROTA_CADASTRO_PROFESSOR
from modulos.academico.academico_db import dbListarCampus

# Interface
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
        st.toast("Professor cadastrado com sucesso!", icon="🎉")

    col1, col2 = st.columns([1, 6])

    with col1:
        if st.button("⬅ Voltar", use_container_width=True):
            st.session_state.pagina = "cadastros" 
            st.rerun()

    if "cache_campus" not in st.session_state:
        st.session_state.cache_campus = dbListarCampus()

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
            
            c1, c2 = st.columns(2)
            with c1:
                nome = st.text_input(
                    "Nome Completo *",
                    placeholder="Ex.: Carlos Mendes",
                    key=f"prof_nome_{st.session_state.form_key_prof}"
                )
                
                cpf = st.text_input(
                    "CPF *",
                    placeholder="Somente números",
                    key=f"prof_cpf_{st.session_state.form_key_prof}"
                )
                
            with c2:
                email = st.text_input(
                    "E-mail *",
                    placeholder="email@exemplo.com",
                    key=f"prof_email_{st.session_state.form_key_prof}"
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
                telefone_tratado = telefone.strip() if telefone.strip() else None

                nova_pessoa = Pessoa(
                    nome=nome.strip(),
                    cpf=cpf.strip(),
                    email=email.strip(),
                    telefone=telefone_tratado
                )
                
                criarProfessor(pessoa=nova_pessoa, idCampus=campus.id)
                
                st.session_state.form_key_prof += 1 
                st.session_state.pop("cache_professores", None)
                st.session_state["cadastro_prof_realizado"] = True
                
                st.rerun()
                
            except SQLAlchemyError as e:
                st.error(f"Erro no banco de dados: {e}")
            except Exception as e:
                st.error(str(e))

# Service
def criarProfessor(pessoa: Pessoa, idCampus: int):
    try:
        if not CPF().validate(pessoa.cpf):
            raise Exception("O CPF disponibilizado não é válido.")
        
        if not validarEmail(pessoa.email):
            raise Exception("O E-mail disponibilizado não é válido.")
            
        if pessoa.telefone:
            if not validarTelefone(pessoa.telefone):
                raise Exception("O telefone disponibilizado não é válido.")

        dbCriarProfessor(pessoa, idCampus)
    
    except SQLAlchemyError:    
        raise
    except Exception:
        raise


# Dados
def dbCriarProfessor(pessoa: Pessoa, idCampus: int):
    with SessionLocal() as session:
        try:
            session.add(pessoa)
            session.commit()
            session.refresh(pessoa)

            professor = Professor(
                pessoa_id = pessoa.id,
                campus_id = idCampus
            )

            session.add(professor)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise