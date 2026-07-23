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

# Interface
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

    col1, col2 = st.columns([1, 6])

    with col1:
        if st.button("⬅ Voltar", use_container_width=True):
            st.session_state.pagina = "cadastros" 
            st.rerun()

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
            
            nome = st.text_input(
                "Nome da Disciplina *",
                placeholder="Ex.: Banco de Dados I",
                key=f"disc_nome_{st.session_state.form_key_disc}"
            )
            
            c1, c2 = st.columns(2)
            with c1:
                carga_horaria = st.number_input(
                    "Carga Horária (Horas) *",
                    min_value=1,
                    value=60,
                    step=10,
                    key=f"disc_carga_{st.session_state.form_key_disc}"
                )
                
            with c2:
                obrigatoria_str = st.selectbox(
                    "Disciplina Obrigatória? *",
                    options=["Sim", "Não"],
                    key=f"disc_obrigatoria_{st.session_state.form_key_disc}"
                )
                obrigatoria = True if obrigatoria_str == "Sim" else False

        st.write("")

        with st.container(border=True):
            st.subheader("🔗 Vínculos e Pré-requisitos")
            
            c3, c4 = st.columns(2)
            with c3:
                curso_selecionado = st.selectbox(
                    "Curso *",
                    options=lista_cursos if lista_cursos else [],
                    format_func=lambda c: c.nome,
                    index=None,
                    placeholder="Selecione um curso...",
                    disabled=not lista_cursos,
                    help="Selecione o curso ao qual esta disciplina pertence.",
                    key=f"disc_curso_{st.session_state.form_key_disc}"
                )
                
            with c4:
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

# Service
def criarDisciplina(disciplina: Disciplina, preRequisitos: list[int]):
    try:
        disciplina.codigo = ""

        if preRequisitos:
            for idPreReq in preRequisitos:
                discPreReq = dbListarDisciplinaId(idPreReq)
                
                if discPreReq == None:
                    raise Exception(f"O id {idPreReq} não corresponde a nenhuma disciplina.")
                
                if discPreReq.curso_id != disciplina.curso_id:
                    raise Exception(f"A disciplina base e seu(s) pre-requisito(s) devem pertencer ao mesmo curso.")
        
            dbCriarDisciplina(disciplina, preRequisitos)
        
        else:
            dbCriarDisciplina(disciplina)

            
    except SQLAlchemyError:    
        raise
    
    except Exception:
        raise

# Dados
def dbCriarDisciplina(disciplina: Disciplina, preRequisitos: list[int] = None):
    with SessionLocal() as session:
        try:
            session.add(disciplina)
            session.commit()
            session.refresh(disciplina)

            disciplina.codigo = f"{disciplina.curso_id}-{disciplina.id:05d}"

            if preRequisitos:
                preReqFinal: list[PreRequisito] = []
                for idPreReq in preRequisitos:
                    preReqFinal.append(PreRequisito(
                        disciplina_id=disciplina.id,
                        prerequisito_id=idPreReq
                    ))
                
                session.add_all(preReqFinal)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise