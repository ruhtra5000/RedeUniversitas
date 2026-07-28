import streamlit as st
from modulos.academico.academico_db import dbListarDisciplinasGeral
from modulos.utils.listagem_utils import separador

# Tela de listagem para Disciplinas
def telaListagemDisciplinas():

    st.title("📋 Listagem de Disciplinas")
    st.caption("Consulte as disciplinas cadastradas no sistema.")

    colVoltar, _ = st.columns([1, 5])

    with colVoltar:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import home_page
            st.switch_page(home_page)

    listaDisciplinas = dbListarDisciplinasGeral()

    if not listaDisciplinas:
        st.info("📖 Nenhuma disciplina cadastrada.")
        return

    st.write("")

    st.caption(
        f"📖 {len(listaDisciplinas)} "
        f"{'disciplina encontrada' if len(listaDisciplinas) == 1 else 'disciplinas encontradas'}"
    )

    proporcoes = [3, 2.2, 3.2, 2.5, 1.3]

    with st.container(border=True):

        h1, h2, h3, h4, h5, h6 = st.columns(
            proporcoes,
            vertical_alignment="center",
        )

        h1.markdown("**Código**")
        h2.markdown("**Disciplina**")
        h3.markdown("**Curso**")
        h4.markdown("**Carga**")
        h5.markdown("**Tipo**")
        h6.markdown("**Ações**")

        separador()

        for indice, disciplina in enumerate(listaDisciplinas):

            c1, c2, c3, c4, c5, c6 = st.columns(
                proporcoes,
                vertical_alignment="center",
            )

            with c1:
                st.write(
                    disciplina.codigo or "Não informado"
                )

            with c2:
                st.markdown(f"**{disciplina.nome}**")

            with c3:
                st.write(
                    disciplina.curso.nome
                    if disciplina.curso
                    else "Não informado"
                )

            with c4:
                st.write(f"{disciplina.carga_horaria} h")

            with c5:
                st.write(
                    "Obrigatória"
                    if disciplina.obrigatoria
                    else "Optativa"
                )

            with c6:
                visualizar = st.button(
                    "👁️",
                    key=f"view_disciplina_{disciplina.id}",
                    help="Visualizar disciplina",
                    use_container_width=True,
                )

            if visualizar:
                st.session_state["disciplina_id"] = disciplina.id

                from modulos.rotas import view_disciplina_page
                st.switch_page(view_disciplina_page)

            if indice < len(listaDisciplinas) - 1:
                separador()