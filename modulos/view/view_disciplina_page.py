import streamlit as st
from modulos.academico.academico_db import (dbListarDisciplinaCodigo, dbListarDisciplinaId, dbListarPreRequisitosDisciplina)
from modulos.utils.view_utils import exibirCampo

# Função para limpar a consulta de disciplina
def limpar_consulta_disciplina():
    st.session_state.pop("consulta_disciplina_id", None)
    st.session_state.pop("consulta_disciplina_codigo", None)
    st.session_state.pop("consulta_disciplina_id_digitado", None)

# Tela de visualização de disciplina
def telaViewDisciplina():

    st.title("🔎 Consulta de Disciplina")
    st.caption("Pesquise uma disciplina pelo código ou pelo ID.")

    if "disciplina_id" in st.session_state:
        st.session_state["consulta_disciplina_id"] = (
            st.session_state.pop("disciplina_id")
        )

    disciplina = None

    col_voltar, _ = st.columns([1, 5])

    with col_voltar:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import listagem_disciplina_page
            st.switch_page(listagem_disciplina_page)

    with st.form("buscar_disciplina", border=True):

        st.markdown("#### 🔍 Buscar disciplina")

        col1, col2 = st.columns(2)

        with col1:
            codigo_digitado = st.text_input(
                "Código",
                placeholder="Ex.: 1-00001",
                key="consulta_disciplina_codigo",
            )

        with col2:
            id_digitado = st.text_input(
                "ID",
                placeholder="Ex.: 1",
                key="consulta_disciplina_id_digitado",
            )

        coluna_botao, _ = st.columns([1.3, 4.7])

        with coluna_botao:
            buscar = st.form_submit_button(
                "🔍 Buscar",
                type="primary",
                use_container_width=True,
            )

    if buscar:

        st.session_state.pop("consulta_disciplina_id", None)

        codigo = codigo_digitado.strip()
        id_disciplina = id_digitado.strip()

        if not codigo and not id_disciplina:
            st.warning("Informe um código ou um ID.")

        elif codigo and id_disciplina:
            st.warning("Informe somente o código ou somente o ID.")

        elif codigo:
            disciplina = dbListarDisciplinaCodigo(codigo)

            if disciplina is None:
                st.error("Disciplina não encontrada.")
            else:
                st.session_state["consulta_disciplina_id"] = disciplina.id

        else:
            if not id_disciplina.isdigit():
                st.error("O ID deve conter somente números.")
            else:
                disciplina = dbListarDisciplinaId(int(id_disciplina))

                if disciplina is None:
                    st.error("Disciplina não encontrada.")
                else:
                    st.session_state["consulta_disciplina_id"] = (
                        disciplina.id
                    )

    disciplina_id = st.session_state.get("consulta_disciplina_id")

    if disciplina is None and disciplina_id is not None:
        disciplina = dbListarDisciplinaId(disciplina_id)

    if disciplina is None:
        if not buscar:
            st.info("Informe um código ou ID para consultar uma disciplina.")
        return

    pre_requisitos = dbListarPreRequisitosDisciplina(disciplina.id)

    st.write("")

    titulo, botao = st.columns(
        [4.7, 1.3],
        vertical_alignment="center",
    )

    with titulo:
        st.subheader(f"📘 {disciplina.nome}")

    with botao:
        st.button(
            "Limpar",
            icon=":material/close:",
            use_container_width=True,
            on_click=limpar_consulta_disciplina,
        )

    with st.container(border=True):

        st.markdown("#### 📚 Dados da Disciplina")

        col1, col2, col3 = st.columns([1, 1.8, 3.2])

        with col1:
            exibir_campo(
                "ID",
                disciplina.id,
            )

        with col2:
            exibir_campo(
                "Código",
                disciplina.codigo or "Não informado",
            )

        with col3:
            exibir_campo(
                "Nome",
                disciplina.nome,
            )

        st.write("")

        col1, col2, col3 = st.columns([1.5, 1.5, 3])

        with col1:
            exibir_campo(
                "Carga Horária",
                f"{disciplina.carga_horaria} horas",
            )

        with col2:
            exibir_campo(
                "Obrigatória",
                "Sim" if disciplina.obrigatoria else "Não",
            )

        with col3:
            exibir_campo(
                "Curso",
                disciplina.curso.nome,
            )

    st.write("")

    with st.container(border=True):

        st.markdown("#### 🔗 Pré-requisitos")

        if not pre_requisitos:
            st.info("Esta disciplina não possui pré-requisitos.")

        else:
            for pre_requisito in pre_requisitos:

                with st.container(border=True):
                    col1, col2 = st.columns(
                        [1.5, 4.5],
                        vertical_alignment="center",
                    )

                    with col1:
                        st.caption("Código")
                        st.markdown(
                            f"**{pre_requisito.codigo or 'Não informado'}**"
                        )

                    with col2:
                        st.caption("Disciplina")
                        st.markdown(f"**{pre_requisito.nome}**")