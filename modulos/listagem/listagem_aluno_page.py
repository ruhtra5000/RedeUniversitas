import streamlit as st
from modulos.academico.academico_service import listarAlunos
from modulos.utils.listagem_utils import separador

# Tela de listagem para Alunos
def telaListagemAlunos():

    st.title(":material/assignment: Listagem de Alunos")
    st.caption("Consulte os alunos cadastrados no sistema.")

    colVoltar, _ = st.columns([1, 5])

    with colVoltar:
        if st.button(":material/arrow_back: Voltar", use_container_width=True):
            from modulos.rotas import home_page
            st.switch_page(home_page)

    listaAlunos = listarAlunos()

    if not listaAlunos:
        st.info(":material/groups: Nenhum aluno cadastrado.")
        return

    st.write("")

    st.caption(
        f":material/groups: {len(listaAlunos)} "
        f"{'aluno encontrado' if len(listaAlunos) == 1 else 'alunos encontrados'}"
    )

    proporcoes = [3, 2.2, 3.2, 2.5, 1.3]

    with st.container(border=True):

        h1, h2, h3, h4, h5 = st.columns(
            proporcoes,
            vertical_alignment="center",
        )

        h1.markdown("**Aluno**")
        h2.markdown("**Matrícula**")
        h3.markdown("**Curso**")
        h4.markdown("**Campus**")
        h5.markdown("**Ações**")

        separador()

        for indice, aluno in enumerate(listaAlunos):

            c1, c2, c3, c4, c5 = st.columns(
                proporcoes,
                vertical_alignment="center",
            )

            with c1:
                st.markdown(f"**{aluno.pessoa.nome}**")

            with c2:
                st.write(
                    aluno.matricula or "Não informado"
                )

            with c3:
                st.write(
                    aluno.curso.nome
                    if aluno.curso
                    else "Não informado"
                )

            with c4:
                st.write(
                    aluno.campus.nome
                    if aluno.campus
                    else "Não informado"
                )

            with c5:
                visualizar = st.button(
                    ":material/visibility:",
                    key=f"view_aluno_{aluno.pessoa_id}",
                    help="Visualizar aluno",
                    use_container_width=True,
                )

            if visualizar:
                st.session_state["aluno_id"] = aluno.pessoa_id

                st.rerun()

            if indice < len(listaAlunos) - 1:
                separador()