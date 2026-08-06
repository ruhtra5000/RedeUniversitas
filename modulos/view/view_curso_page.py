import streamlit as st
from modulos.academico.academico_service import listarCursoId
from modulos.utils.view_utils import exibirCampo, formatar_modalidade, formatar_mensalidade, limpar_consulta_curso

# Tela de visualização de curso
def telaViewCurso():

    st.title("🔎 Consulta de Curso")
    st.caption("Pesquise um curso pelo ID.")

    if "curso_id" in st.session_state:
        st.session_state["consulta_curso_id"] = st.session_state.pop("curso_id")

    curso = None

    col_voltar, _ = st.columns([1, 5])

    with col_voltar:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import listagem_cursos_page
            st.switch_page(listagem_cursos_page)

    with st.form("buscar_curso", border=True):

        st.markdown("#### 🔍 Buscar curso")

        id_digitado = st.text_input(
            "ID do Curso",
            placeholder="Ex.: 1",
            key="consulta_curso_busca",
        )

        coluna_botao, _ = st.columns([1.3, 4.7])

        with coluna_botao:
            buscar = st.form_submit_button(
                "🔍 Buscar",
                type="primary",
                use_container_width=True,
            )

    if buscar:

        st.session_state.pop("consulta_curso_id", None)

        id_curso = id_digitado.strip()

        if not id_curso:
            st.warning("Informe o ID do curso.")

        elif not id_curso.isdigit():
            st.error("O ID deve conter somente números.")

        else:
            curso = listarCursoId(int(id_curso))

            if curso is None:
                st.error("Curso não encontrado.")
            else:
                st.session_state["consulta_curso_id"] = curso.id

    curso_id = st.session_state.get("consulta_curso_id")

    if curso is None and curso_id is not None:
        curso = listarCursoId(curso_id)

    if curso is None:
        if not buscar:
            st.info("Informe um ID para consultar um curso.")
        return

    st.write("")

    titulo, botao = st.columns(
        [4.7, 1.3],
        vertical_alignment="center",
    )

    with titulo:
        st.subheader(f"📚 {curso.nome}")

    with botao:
        st.button(
            "Limpar",
            icon=":material/close:",
            use_container_width=True,
            on_click=limpar_consulta_curso,
        )

    with st.container(border=True):

        st.markdown("#### 📚 Dados Principais")

        col1, col2, col3 = st.columns([1, 3.2, 1.8])

        with col1:
            exibirCampo("ID", curso.id)

        with col2:
            exibirCampo("Nome", curso.nome)

        with col3:
            exibirCampo(
                "Modalidade",
                formatar_modalidade(curso.modalidade),
            )

        st.write("")

        col1, col2, col3 = st.columns(3)

        with col1:
            exibirCampo(
                "Mensalidade Base",
                formatar_mensalidade(curso.mensalidade_base),
            )

        with col2:
            exibirCampo(
                "Carga Horária",
                f"{curso.carga_horaria} horas",
            )

        with col3:
            exibirCampo(
                "Duração",
                (
                    f"{curso.dur_min_semestre} a "
                    f"{curso.dur_max_semestre} semestres"
                ),
            )

    st.write("")

    with st.container(border=True):

        st.markdown("#### 🔗 Vínculos Institucionais")

        nome_coordenador = (
            curso.coordenador.pessoa.nome
            if curso.coordenador is not None
            else "Nenhum coordenador definido"
        )

        col1, col2 = st.columns(2)

        with col1:
            exibirCampo(
                "Campus",
                curso.campus.nome,
            )

        with col2:
            exibirCampo(
                "Coordenador",
                nome_coordenador,
            )