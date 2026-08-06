import streamlit as st
from modulos.academico.academico_service import listarProfessores
from modulos.utils.listagem_utils import formatar_cpf, separador

# Tela de listagem para Professores
def telaListagemProfessores():

    st.title("📋 Listagem de Professores")
    st.caption("Consulte os professores cadastrados no sistema.")

    colVoltar, _ = st.columns([1, 5])

    with colVoltar:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import home_page
            st.switch_page(home_page)

    listaProfessores = listarProfessores()

    if not listaProfessores:
        st.info("👨‍🏫 Nenhum professor cadastrado.")
        return

    st.write("")

    st.caption(
        f"👨‍🏫 {len(listaProfessores)} "
        f"{'professor encontrado' if len(listaProfessores) == 1 else 'professores encontrados'}"
    )

    proporcoes = [3, 2.2, 3.2, 2.5, 1.3]

    with st.container(border=True):

        h1, h2, h3, h4, h5 = st.columns(
            proporcoes,
            vertical_alignment="center",
        )

        h1.markdown("**Professor**")
        h2.markdown("**CPF**")
        h3.markdown("**E-mail**")
        h4.markdown("**Campus**")
        h5.markdown("**Ações**")

        separador()

        for indice, professor in enumerate(listaProfessores):

            c1, c2, c3, c4, c5 = st.columns(
                proporcoes,
                vertical_alignment="center",
            )

            with c1:
                st.markdown(f"**{professor.pessoa.nome}**")

            with c2:
                st.write(formatar_cpf(professor.pessoa.cpf))

            with c3:
                st.write(
                    professor.pessoa.email or "Não informado"
                )

            with c4:
                st.write(
                    professor.campus.nome
                    if professor.campus
                    else "Não informado"
                )

            with c5:
                visualizar = st.button(
                    "👁️",
                    key=f"view_professor_{professor.pessoa_id}",
                    help="Visualizar professor",
                    use_container_width=True,
                )

            if visualizar:
                st.session_state["professor_id"] = (
                    professor.pessoa_id
                )

                from modulos.rotas import view_professor_page
                st.switch_page(view_professor_page)

            if indice < len(listaProfessores) - 1:
                separador()