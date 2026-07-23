from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from validate_docbr.CPF import CPF
from database.Conexao import SessionLocal
import database.entidades
from database.entidades.Pessoa import Pessoa
from database.entidades.Aluno import Aluno
from database.entidades.Campus import Campus
from database.entidades.Curso import Curso
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
from modulos.academico.academico_db import dbExisteCpf, dbExisteEmail, dbListarCampus, dbListarCursos

# Interface
def telaCadastroAluno():

    if "form_key_aluno" not in st.session_state:
        st.session_state.form_key_aluno = 0

    st.title("🎓 Cadastro de Aluno")
    st.caption("Preencha as informações abaixo para cadastrar um novo aluno.")

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
    
    if st.session_state.pop("cadastro_realizado", False):
        st.toast("Aluno cadastrado com sucesso!", icon="🎉")

    col1, col2 = st.columns([1, 6])

    with col1:
        if st.button("⬅ Voltar", use_container_width=True):
            st.session_state.pagina = "cadastros"
            st.rerun()

    if "cache_campus" not in st.session_state:
        st.session_state.cache_campus = dbListarCampus()

    if "cache_cursos" not in st.session_state:
        st.session_state.cache_cursos = dbListarCursos()

    lista_campus = st.session_state.cache_campus
    lista_cursos = st.session_state.cache_cursos

    if not lista_campus or not lista_cursos:
        st.warning(
            """
            ⚠️ Antes de cadastrar um aluno é necessário possuir:

            - Pelo menos **1 Campus**
            - Pelo menos **1 Curso**
            """
        )

    with st.form(f"cadastro_aluno_{st.session_state.form_key_aluno}", border=False):

        # Dados pessoais

        with st.container(border=True):
            st.subheader("👤 Dados Pessoais")
            c1, c2 = st.columns(2)

            with c1:
                nome = st.text_input(
                    "Nome Completo *",
                    placeholder="Ex.: João da Silva",
                    key=f"aluno_nome_{st.session_state.form_key_aluno}"
                )

                cpf = st.text_input(
                    "CPF *",
                    placeholder="Somente números",
                    key=f"aluno_cpf_{st.session_state.form_key_aluno}"
                )

            with c2:
                email = st.text_input(
                    "E-mail *",
                    placeholder="email@exemplo.com",
                    key=f"aluno_email_{st.session_state.form_key_aluno}"
                )

                telefone = st.text_input(
                    "Telefone",
                    placeholder="Opcional",
                    key=f"aluno_telefone_{st.session_state.form_key_aluno}"
                )

        st.write("")

        # Dados acadêmicos

        with st.container(border=True):
            st.subheader("🎓 Dados Acadêmicos")
            c1, c2 = st.columns(2)

            with c1:
                campus = st.selectbox(
                    "Campus *",
                    options=lista_campus if lista_campus else [],
                    format_func=lambda x: x.nome,
                    index=None,
                    placeholder="Selecione um campus...",
                    disabled=not lista_campus,
                    key=f"aluno_campus_{st.session_state.form_key_aluno}"
                )

            with c2:
                curso = st.selectbox(
                    "Curso *",
                    options=lista_cursos if lista_cursos else [],
                    format_func=lambda x: x.nome,
                    index=None,
                    placeholder="Selecione um curso...",
                    disabled=not lista_cursos,
                    key=f"aluno_curso_{st.session_state.form_key_aluno}"
                )

        st.write("")

        _, centro, _ = st.columns([2, 3, 2])

        with centro:
            cadastrar = st.form_submit_button(
                "💾 Cadastrar Aluno",
                use_container_width=True,
                type="primary"
            )

    # Processamento

    if cadastrar:
        if not lista_campus or not lista_cursos:
            st.error("Cadastre pelo menos um Campus e um Curso antes de continuar.")

        elif not nome.strip() or not cpf.strip() or not email.strip():
            st.error("Preencha todos os campos obrigatórios (Nome, CPF e E-mail).")
            
        elif campus is None:
            st.error("Por favor, selecione um Campus.")
            
        elif curso is None:
            st.error("Por favor, selecione um Curso.")

        else:
            try:
                nova_pessoa = Pessoa(
                    nome=nome.strip(),
                    cpf=cpf.strip(),
                    email=email.strip(),
                    telefone=telefone.strip()
                )

                criarAluno(
                    pessoa=nova_pessoa,
                    idCampus=campus.id,
                    idCurso=curso.id
                )

                st.session_state.form_key_aluno += 1 
                st.session_state["cadastro_realizado"] = True
                st.rerun()

            except SQLAlchemyError:
                st.error("Erro ao salvar os dados no banco.")

            except Exception as e:
                st.error(str(e))
                
# Service
def criarAluno(pessoa: Pessoa, idCampus: int, idCurso: int):
    try:
        if not CPF().validate(pessoa.cpf):
            raise Exception("O CPF disponibilizado não é válido.")
        
        if dbExisteCpf(pessoa.cpf):
            raise Exception("Já existe um aluno cadastrado com este CPF.")
        
        if not validarEmail(pessoa.email):
            raise Exception("O E-mail disponibilizado não é válido.")
        
        if dbExisteEmail(pessoa.email):
            raise Exception("Já existe um aluno cadastrado com este e-mail.")
            
        if pessoa.telefone != "":
            if not validarTelefone(pessoa.telefone):
                raise Exception("O telefone disponibilizado não é válido.")
                
        dbCriarAluno(pessoa, idCampus, idCurso)
    
    except SQLAlchemyError:    
        raise

    except Exception:
        raise


# Dados
def dbCriarAluno(pessoa: Pessoa, idCampus: int, idCurso: int):
    anoAtual = datetime.now().year

    with SessionLocal() as session:
        try:
            session.add(pessoa)
            session.commit()
            session.refresh(pessoa)

            aluno = Aluno(
                pessoa_id = pessoa.id,
                matricula = f"{anoAtual}-{pessoa.id:05d}",
                campus_id = idCampus,
                curso_id = idCurso
            )

            session.add(aluno)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise