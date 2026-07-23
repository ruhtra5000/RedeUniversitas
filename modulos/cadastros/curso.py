from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from database.Conexao import SessionLocal
from database.entidades.Curso import Curso
from database.entidades.enums.ModalidadeCurso import ModalidadeCurso
from modulos.academico.academico_db import (dbListarCursos,dbListarProfessorId,dbListarCampus,dbListarProfessores)
import database.entidades

# Interface
def telaCadastroCurso():

    if "form_key_curso" not in st.session_state:
        st.session_state.form_key_curso = 0

    st.title("📚 Cadastro de Curso")
    st.caption("Preencha as informações abaixo para cadastrar um novo curso.")

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

    if st.session_state.pop("cadastro_curso_realizado", False):
        st.toast("Curso cadastrado com sucesso!", icon="🎉")

    if "cache_campus" not in st.session_state:
        st.session_state.cache_campus = dbListarCampus()

    if "cache_professores" not in st.session_state:
        st.session_state.cache_professores = dbListarProfessores()

    lista_campus = st.session_state.cache_campus
    lista_professores = st.session_state.cache_professores

    col1, col2 = st.columns([1, 6])

    with col1:
        if st.button("⬅ Voltar", use_container_width=True):
            st.session_state.pagina = "cadastros" 
            st.rerun()

    with st.form(key=f"cadastro_curso_{st.session_state.form_key_curso}", border=False):

        # Dados do Curso
        with st.container(border=True):
            st.subheader("📚 Dados Principais")
            
            nome = st.text_input(
                "Nome do Curso *",
                placeholder="Ex.: Engenharia de Software",
                key=f"curso_nome_{st.session_state.form_key_curso}"
            )
            
            c1, c2, c3 = st.columns(3)
            with c1:
                modalidade = st.selectbox(
                    "Modalidade *",
                    options=list(ModalidadeCurso), 
                    format_func=lambda x: x.name.replace("_", " ").title(),
                    key=f"curso_modalidade_{st.session_state.form_key_curso}"
                )
            with c2:
                mensalidade_base = st.number_input(
                    "Mensalidade Base (R$) *",
                    min_value=1.0, 
                    step=50.0,
                    format="%.2f",
                    key=f"curso_mensalidade_{st.session_state.form_key_curso}"
                )
            with c3:
                carga_horaria = st.number_input(
                    "Carga Horária Total (Horas) *",
                    min_value=1,
                    step=100,
                    key=f"curso_carga_{st.session_state.form_key_curso}"
                )
                
            c4, c5 = st.columns(2)
            with c4:
                dur_min = st.number_input(
                    "Duração Mínima (Semestres) *",
                    min_value=1,
                    step=1,
                    key=f"curso_dur_min_{st.session_state.form_key_curso}"
                )
            with c5:
                dur_max = st.number_input(
                    "Duração Máxima (Semestres) *",
                    min_value=1,
                    step=1,
                    key=f"curso_dur_max_{st.session_state.form_key_curso}"
                )

        st.write("")

        # Vínculos Institucionais
        with st.container(border=True):
            st.subheader("🔗 Vínculos Institucionais")
            
            c1, c2 = st.columns(2)
            with c1:
                campus_selecionado = st.selectbox(
                    "Campus *", 
                    options=lista_campus,
                    format_func=lambda c: c.nome,
                    index=None,
                    placeholder="Selecione um campus...",
                    key=f"curso_campus_{st.session_state.form_key_curso}"
                )
                
            with c2:
                opcoes_professores = [None] + lista_professores
                
                coordenador_selecionado = st.selectbox(
                    "Coordenador (Opcional)", 
                    options=opcoes_professores,
                    format_func=lambda p: "Nenhum" if p is None else p.pessoa.nome,
                    index=0,
                    help="Selecione o professor coordenador deste curso.",
                    key=f"curso_coord_{st.session_state.form_key_curso}"
                )

        st.write("")

        _, centro, _ = st.columns([2, 3, 2])
        
        with centro:
            cadastrar = st.form_submit_button(
                "💾 Cadastrar Curso", 
                type="primary", 
                use_container_width=True
            )

    # Processamento
    if cadastrar:
        if not nome.strip():
            st.error("Por favor, informe o Nome do Curso.")
        elif campus_selecionado is None:
            st.error("Por favor, selecione o Campus vinculado.")
        elif dur_min > dur_max:
            st.error("A duração mínima não pode ser maior que a duração máxima.")
        else:
            try:
                id_campus = campus_selecionado.id
                id_coordenador = coordenador_selecionado.pessoa_id if coordenador_selecionado else None

                novo_curso = Curso(
                    nome=nome.strip(),
                    modalidade=modalidade,
                    mensalidade_base=mensalidade_base,
                    carga_horaria=carga_horaria,
                    dur_min_semestre=dur_min,
                    dur_max_semestre=dur_max,
                    campus_id=id_campus,
                    coordenador_id=id_coordenador
                )
                
                criarCurso(curso=novo_curso)
                
                st.session_state.form_key_curso += 1 
                st.session_state.pop("cache_cursos", None)
                st.session_state["cadastro_curso_realizado"] = True
                st.rerun()
                
            except SQLAlchemyError as e:
                st.error(f"Erro no banco de dados: {e}")
            except Exception as e:
                st.error(str(e))

# Service
def criarCurso(curso: Curso):
    try:
        if curso.coordenador_id:  
            coordenador = dbListarProfessorId(curso.coordenador_id)

            if not coordenador:
                raise Exception("O ID do Coordenador informado não existe no sistema.")

            if coordenador.campus_id != curso.campus_id:
                raise Exception("O coordenador do curso deve estar vinculado ao mesmo campus do curso.")

        dbCriarCurso(curso)
            
    except SQLAlchemyError:    
        raise
    
    except Exception:
        raise


# Dados
def dbCriarCurso(curso: Curso):
    with SessionLocal() as session:
        try:
            session.add(curso)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise