import streamlit as st
from modulos.academico.academico_service import listarCursos
from modulos.utils.listagem_utils import formatar_modalidade, separador

# Tela de listagem para Cursos
def telaListagemCursos():

    st.title("📋 Listagem de Cursos")
    st.caption("Consulte os cursos cadastrados no sistema.")

    colVoltar, _ = st.columns([1, 5])

    with colVoltar:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import home_page
            st.switch_page(home_page)

    listaCursos = listarCursos()

    if not listaCursos:
        st.info("📚 Nenhum curso cadastrado.")
        return

    st.write("")

    st.caption(
        f"📚 {len(listaCursos)} "
        f"{'curso encontrado' if len(listaCursos) == 1 else 'cursos encontrados'}"
    )

    proporcoes = [3, 2.2, 3.2, 2.5, 1.3]

    with st.container(border=True):

        # Cabeçalho
        h1, h2, h3, h4, h5 = st.columns(
            proporcoes,
            vertical_alignment="center",
        )

        h1.markdown("**Curso**")
        h2.markdown("**Modalidade**")
        h3.markdown("**Campus**")
        h4.markdown("**Carga**")
        h5.markdown("**Ações**")

        separador()

        # Linhas
        for indice, curso in enumerate(listaCursos):

            c1, c2, c3, c4, c5 = st.columns(
                proporcoes,
                vertical_alignment="center",
            )

            with c1:
                st.markdown(f"**{curso.nome}**")

            with c2:
                st.write(formatar_modalidade(curso.modalidade))

            with c3:
                st.write(curso.campus.nome)

            with c4:
                st.write(f"{curso.carga_horaria} h")

            with c5:
                visualizar = st.button(
                    "👁️",
                    key=f"view_curso_{curso.id}",
                    help="Visualizar curso",
                    use_container_width=True,
                )

            if visualizar:
                st.session_state["curso_id"] = curso.id

                st.rerun()

            if indice < len(listaCursos) - 1:
                separador()