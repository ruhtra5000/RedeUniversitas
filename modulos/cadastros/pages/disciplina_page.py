from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from database.Conexao import SessionLocal
from database.entidades.Curso import Curso
from database.entidades.Disciplina import Disciplina
from database.entidades.PreRequisito import PreRequisito
from modulos.academico.academico_db import dbListarDisciplinaId
from modulos.academico.academico_db import dbListarDisciplinasGeral
import database.entidades
from modulos.academico.academico_db import dbListarCursos
from modulos.cadastros.disciplina import criarDisciplina

def telaCadastroDisciplina():

    if "form_key_disc" not in st.session_state:
        st.session_state.form_key_disc = 0

    st.title("📘 Cadastro de Disciplina")
    st.caption("Preencha as informações abaixo para cadastrar uma nova disciplina no curso.")

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

    if st.session_state.pop("cadastro_disc_realizado", False):
        st.toast("Disciplina cadastrada com sucesso!", icon="🎉")

    col1, _ = st.columns([1, 6])

    with col1:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import cadastros_page # evita import circular
            st.switch_page(cadastros_page)

    if "cache_cursos" not in st.session_state:
        st.session_state.cache_cursos = dbListarCursos()

    if "cache_disciplinas" not in st.session_state:
        st.session_state.cache_disciplinas = dbListarDisciplinasGeral()

    lista_cursos = st.session_state.cache_cursos
    lista_disciplinas_existentes = st.session_state.cache_disciplinas

    if not lista_cursos:
        st.warning(
            """
            ⚠️ Antes de cadastrar uma disciplina é necessário possuir:

            - Pelo menos **1 Curso**
            """
        )

    with st.form(key=f"cadastro_disc_{st.session_state.form_key_disc}", border=False):

        with st.container(border=True):
            st.subheader("📚 Dados da Disciplina")
            
            with st.container(horizontal=True):
                nome = st.text_input(
                    "Nome da Disciplina *",
                    placeholder="Ex.: Banco de Dados I",
                    key=f"disc_nome_{st.session_state.form_key_disc}"
                )
                codigo = st.text_input(
                    "Código *",
                    placeholder="Ex.: LOG-01",
                    key=f"disc_codigo_{st.session_state.form_key_disc}"
                )

        st.write("")

        with st.container(border=True):
            st.subheader("🎓 Vínculo e Carga Horária")

            with st.container(horizontal=True):
                curso_selecionado = st.selectbox(
                    "Curso Vinculado *",
                    options=lista_cursos if lista_cursos else [],
                    format_func=lambda c: c.nome,
                    index=None,
                    placeholder="Selecione um curso...",
                    disabled=not lista_cursos,
                    key=f"disc_curso_{st.session_state.form_key_disc}"
                )
                carga_horaria = st.number_input(
                    "Carga Horária (Horas) *",
                    min_value=1,
                    value=60,
                    step=10,
                    key=f"disc_ch_{st.session_state.form_key_disc}"
                )
            
            obrigatoria_str = st.selectbox(
                "Disciplina Obrigatória? *",
                options=["Sim", "Não"],
                key=f"disc_obrigatoria_{st.session_state.form_key_disc}"
            )
            obrigatoria = True if obrigatoria_str == "Sim" else False

            
            pre_requisitos_selecionados = st.multiselect(
                "Pré-requisitos",
                options=lista_disciplinas_existentes,
                format_func=lambda d: d.nome,
                placeholder="Selecione uma ou mais disciplinas...",
                help="Opcional. Selecione as disciplinas que são pré-requisito.",
                key=f"disc_prereq_{st.session_state.form_key_disc}"
            )

        st.write("")

        _, centro, _ = st.columns([2, 3, 2])
        
        with centro:
            cadastrar = st.form_submit_button(
                "💾 Cadastrar Disciplina", 
                type="primary", 
                use_container_width=True
            )

    # Processamento
    if cadastrar:
        if not lista_cursos:
            st.error("Cadastre pelo menos um Curso antes de continuar.")
        elif not nome.strip():
            st.error("Por favor, preencha o Nome da Disciplina.")
        elif curso_selecionado is None:
            st.error("Por favor, selecione um Curso.")
        else:
            try:
                curso_id = curso_selecionado.id
                lista_pre_req_ids = [disc.id for disc in pre_requisitos_selecionados]

                nova_disciplina = Disciplina(
                    nome=nome.strip(),
                    carga_horaria=carga_horaria,
                    obrigatoria=obrigatoria,
                    curso_id=curso_id,
                    codigo="" 
                )
                
                criarDisciplina(disciplina=nova_disciplina, preRequisitos=lista_pre_req_ids)
                
                st.session_state.form_key_disc += 1 
                st.session_state.pop("cache_disciplinas", None)
                st.session_state["cadastro_disc_realizado"] = True
                st.rerun()
                
            except Exception as e:
                st.error(str(e))