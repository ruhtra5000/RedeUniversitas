import streamlit as st
from modulos.academico.academico_service import listarMatriculasGeral
from modulos.utils.listagem_utils import separador, formatar_aprovacao

# Tela de listagem de matrículas
def telaListagemMatriculas():

    st.title(":material/assignment: Listagem de Matrículas")
    st.caption("Consulte as matrículas acadêmicas.")

    colVoltar, _ = st.columns([1, 5])

    with colVoltar:
        if st.button(":material/arrow_back: Voltar", use_container_width=True):
            from modulos.rotas import home_page
            st.switch_page(home_page)

    listaMatriculas = listarMatriculasGeral()

    if not listaMatriculas:
        st.info(":material/edit_document: Nenhuma matrícula cadastrada.")
        return

    st.write("")

    st.caption(
        f":material/edit_document: {len(listaMatriculas)} "
        f"{'matrícula encontrada' if len(listaMatriculas) == 1 else 'matrículas encontradas'}"
    )

    proporcoes = [3, 2.2, 3.2, 2.5, 1.3]

    with st.container(border=True):

        h1, h2, h3, h4, h5 = st.columns(
            proporcoes,
            vertical_alignment="center",
        )

        h1.markdown("**Aluno**")
        h2.markdown("**Disciplina**")
        h3.markdown("**Turma**")
        h4.markdown("**Situação**")
        h5.markdown("**Ações**")

        separador()

        for indice, matricula in enumerate(listaMatriculas):

            c1, c2, c3, c4, c5 = st.columns(
                proporcoes,
                vertical_alignment="center",
            )

            with c1:
                st.markdown(
                    f"**{matricula.aluno.pessoa.nome}**"
                )

            with c2:
                st.write(matricula.disciplina.nome)

            with c3:
                st.write(
                    matricula.turma.codigo or
                    f"Turma {matricula.turma_id}"
                )

            with c4:
                st.write(
                    formatar_aprovacao(matricula.aprovacao)
                )

            with c5:
                visualizar = st.button(
                    ":material/visibility:",
                    key=(
                        f"view_matricula_"
                        f"{matricula.aluno_id}_"
                        f"{matricula.turma_id}"
                    ),
                    help="Visualizar matrícula",
                    use_container_width=True,
                )

            if visualizar:
                st.session_state["matricula_selecionada"] = {
                    "aluno_id": matricula.aluno_id,
                    "turma_id": matricula.turma_id,
                }

                st.rerun()

            if indice < len(listaMatriculas) - 1:
                separador()