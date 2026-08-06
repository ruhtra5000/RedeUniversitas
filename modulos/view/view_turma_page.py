import streamlit as st
from modulos.academico.academico_service import listarTurmaCodigo, listarTurmaId
from modulos.utils.view_utils import exibirCampo, limpar_consulta_turma

# Tela de visualização de turma
def telaViewTurma():

    st.title("🔎 Consulta de Turma")
    st.caption("Pesquise uma turma pelo código ou pelo ID.")
    if "turma_id" in st.session_state:
        st.session_state["consulta_turma_id"] = (
            st.session_state.pop("turma_id")
        )

    turma = None

    col_voltar, _ = st.columns([1, 5])

    with col_voltar:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import listagem_turma_page
            st.switch_page(listagem_turma_page)

    with st.form("buscar_turma", border=True):

        st.markdown("#### 🔍 Buscar turma")

        col1, col2 = st.columns(2)

        with col1:
            codigo_digitado = st.text_input(
                "Código",
                placeholder="Ex.: 1-00001",
                key="consulta_turma_codigo",
            )

        with col2:
            id_digitado = st.text_input(
                "ID",
                placeholder="Ex.: 1",
                key="consulta_turma_id_digitado",
            )

        coluna_botao, _ = st.columns([1.3, 4.7])

        with coluna_botao:
            buscar = st.form_submit_button(
                "🔍 Buscar",
                type="primary",
                use_container_width=True,
            )

    if buscar:

        st.session_state.pop("consulta_turma_id", None)

        codigo = codigo_digitado.strip()
        id_turma = id_digitado.strip()

        if not codigo and not id_turma:
            st.warning("Informe um código ou um ID.")

        elif codigo and id_turma:
            st.warning(
                "Informe somente o código ou somente o ID."
            )

        elif codigo:
            turma = listarTurmaCodigo(codigo)

            if turma is None:
                st.error("Turma não encontrada.")
            else:
                st.session_state["consulta_turma_id"] = turma.id

        else:
            if not id_turma.isdigit():
                st.error("O ID deve conter somente números.")
            else:
                turma = listarTurmaId(int(id_turma))

                if turma is None:
                    st.error("Turma não encontrada.")
                else:
                    st.session_state["consulta_turma_id"] = turma.id

    turma_id = st.session_state.get("consulta_turma_id")

    if turma is None and turma_id is not None:
        turma = listarTurmaId(turma_id)

    if turma is None:
        if not buscar:
            st.info(
                "Informe um código ou ID para consultar uma turma."
            )

        return

    st.write("")

    titulo, botao = st.columns(
        [4.7, 1.3],
        vertical_alignment="center",
    )

    with titulo:
        titulo_turma = turma.codigo or f"Turma {turma.id}"
        st.subheader(f"🏫 {titulo_turma}")

    with botao:
        st.button(
            "Limpar",
            icon=":material/close:",
            use_container_width=True,
            on_click=limpar_consulta_turma,
        )

    with st.container(border=True):

        st.markdown("#### 🏫 Dados da Turma")

        col1, col2, col3 = st.columns([1, 2.5, 2.5])

        with col1:
            exibirCampo(
                "ID",
                turma.id,
            )

        with col2:
            exibirCampo(
                "Código",
                turma.codigo or "Não informado",
            )

        with col3:
            exibirCampo(
                "Semestre",
                turma.semestre,
            )

    st.write("")

    with st.container(border=True):

        st.markdown("#### 🔗 Vínculos Acadêmicos")

        col1, col2 = st.columns(2)

        with col1:
            exibirCampo(
                "Curso",
                turma.curso.nome,
            )

        with col2:
            exibirCampo(
                "Disciplina",
                turma.disciplina.nome,
            )

        st.write("")

        exibirCampo(
            "Professor",
            turma.professor.pessoa.nome,
        )