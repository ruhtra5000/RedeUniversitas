from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from database.entidades.Curso import ModalidadeCurso
from modulos.academico.academico_service import listarCursoId, editarCurso

def telaEdicaoCurso():
    if "ADMIN" not in st.session_state.roles:
        st.error("Acesso negado. Apenas administradores podem editar registros.")
        st.stop()

    curso_id = st.session_state.get("edicao_curso_id")
    if not curso_id:
        st.error("Curso não especificado para edição.")
        if st.button("Voltar"):
            from modulos.rotas import view_curso_page
            st.switch_page(view_curso_page)
        st.stop()

    curso = listarCursoId(curso_id)
    if not curso:
        st.error("Curso não encontrado.")
        st.stop()

    if "form_key_edit_curso" not in st.session_state:
        st.session_state.form_key_edit_curso = 0

    col1, _ = st.columns([1, 6])
    with col1:
        if st.button(":material/arrow_back: Voltar", width="stretch"):
            st.session_state["consulta_curso_id"] = curso_id
            from modulos.rotas import view_curso_page
            st.switch_page(view_curso_page)

    st.title(":material/edit: Editar Curso")
    st.caption("Altere os dados do curso.")

    if st.session_state.pop("edicao_realizada", False):
        st.toast("Dados do curso atualizados com sucesso!", icon=":material/check:")

    with st.container():
        with st.container():
            st.subheader("Informações Básicas")
            with st.container(horizontal=True):
                nome = st.text_input(
                    "Nome do Curso *",
                    value=curso.nome,
                    key=f"edit_curso_nome_{st.session_state.form_key_edit_curso}"
                )
                
                modalidades = [m.value for m in ModalidadeCurso]
                modalidade_index = modalidades.index(curso.modalidade.value) if curso.modalidade else 0
                modalidade = st.selectbox(
                    "Modalidade *",
                    options=modalidades,
                    index=modalidade_index,
                    key=f"edit_curso_modalidade_{st.session_state.form_key_edit_curso}"
                )

            st.subheader("Configurações Acadêmicas")
            with st.container(horizontal=True):
                mensalidade_base = st.number_input(
                    "Mensalidade Base (R$) *",
                    min_value=0.0,
                    value=float(curso.mensalidade_base),
                    step=100.0,
                    key=f"edit_curso_mensalidade_{st.session_state.form_key_edit_curso}"
                )
                
            with st.container(horizontal=True):
                carga_horaria = st.number_input(
                    "Carga Horária Total (h) *",
                    min_value=1,
                    value=curso.carga_horaria,
                    key=f"edit_curso_carga_horaria_{st.session_state.form_key_edit_curso}"
                )
                duracao_min = st.number_input(
                    "Duração Mínima (Semestres) *",
                    min_value=1,
                    value=curso.dur_min_semestre,
                    key=f"edit_curso_duracao_min_{st.session_state.form_key_edit_curso}"
                )
                duracao_max = st.number_input(
                    "Duração Máxima (Semestres) *",
                    min_value=1,
                    value=curso.dur_max_semestre,
                    key=f"edit_curso_duracao_max_{st.session_state.form_key_edit_curso}"
                )

            st.subheader("Vínculo Institucional")
            st.text_input(
                "Campus",
                value=curso.campus.nome if curso.campus else "",
                disabled=True,
                help="O campus do curso não pode ser alterado diretamente.",
                key=f"edit_curso_campus_{st.session_state.form_key_edit_curso}"
            )

        st.write("")
        _, centro, _ = st.columns([2, 3, 2])

        with centro:
            salvar = st.button(
                "Salvar Alterações",
                width="stretch",
                type="primary",
                key=f"btn_edit_curso_{st.session_state.form_key_edit_curso}"
            )

    if salvar:
        if not nome.strip():
            st.error("Preencha o Nome do Curso.")
        elif duracao_min > duracao_max:
            st.error("A duração mínima não pode ser maior que a máxima.")
        else:
            try:
                mod_enum = ModalidadeCurso(modalidade)
                editarCurso(
                    idCurso=curso.id,
                    nome=nome.strip(),
                    modalidade=mod_enum,
                    mensalidade_base=mensalidade_base,
                    carga_horaria=carga_horaria,
                    dur_min_semestre=duracao_min,
                    dur_max_semestre=duracao_max
                )
                st.session_state.form_key_edit_curso += 1 
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(f"{str(e)}")
