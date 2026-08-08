import streamlit as st
from modulos.academico.academico_service import listarTurmasGeral
from modulos.utils.listagem_utils import separador

# Tela de listagem para Turmas
def telaListagemTurmas():

    st.title("📋 Listagem de Turmas")
    st.caption("Consulte as turmas cadastradas no sistema.")

    colVoltar, _ = st.columns([1, 5])

    with colVoltar:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import home_page
            st.switch_page(home_page)

    listaTurmas = listarTurmasGeral()

    if not listaTurmas:
        st.info("🏫 Nenhuma turma cadastrada.")
        return

    st.write("")

    st.caption(
        f"🏫 {len(listaTurmas)} "
        f"{'turma encontrada' if len(listaTurmas) == 1 else 'turmas encontradas'}"
    )

    proporcoes = [3, 2.2, 3.2, 2.5, 1.3]

    with st.container(border=True):

        h1, h2, h3, h4, h5 = st.columns(
            proporcoes,
            vertical_alignment="center",
        )

        h1.markdown("**Código**")
        h2.markdown("**Disciplina**")
        h3.markdown("**Professor**")
        h4.markdown("**Semestre**")
        h5.markdown("**Ações**")

        separador()

        for indice, turma in enumerate(listaTurmas):

            c1, c2, c3, c4, c5 = st.columns(
                proporcoes,
                vertical_alignment="center",
            )

            with c1:
                st.write(turma.codigo or "Não informado")

            with c2:
                st.markdown(f"**{turma.disciplina.nome}**")

            with c3:
                st.write(turma.professor.pessoa.nome)

            with c4:
                st.write(turma.semestre)

            with c5:
                visualizar = st.button(
                    "👁️",
                    key=f"view_turma_{turma.id}",
                    help="Visualizar turma",
                    use_container_width=True,
                )

            if visualizar:
                st.session_state["turma_id"] = turma.id

                st.rerun()

            if indice < len(listaTurmas) - 1:
                separador()