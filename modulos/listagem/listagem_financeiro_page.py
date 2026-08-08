import streamlit as st
from modulos.financeiro.financeiro_service import listarFinanceiro
from modulos.utils.listagem_utils import formatar_cpf, separador

# Tela de listagem para Financeiros
def telaListagemFinanceiros():

    st.title(":material/assignment: Listagem do Financeiro")
    st.caption("Consulte os funcionários do financeiro.")


    listaFinanceiros = listarFinanceiro()

    if not listaFinanceiros:
        st.info(":material/payments: Nenhum funcionário financeiro cadastrado.")
        return

    st.write("")

    st.caption(
        f":material/payments: {len(listaFinanceiros)} "
        f"{'funcionário encontrado' if len(listaFinanceiros) == 1 else 'funcionários encontrados'}"
    )

    proporcoes = [3, 2.2, 3.2, 2.5, 1.3]

    with st.container(border=True):

        h1, h2, h3, h4, h5 = st.columns(
            proporcoes,
            vertical_alignment="center",
        )

        h1.markdown("**Funcionário**")
        h2.markdown("**CPF**")
        h3.markdown("**E-mail**")
        h4.markdown("**Campus**")
        h5.markdown("**Ações**")

        separador()

        for indice, financeiro in enumerate(listaFinanceiros):

            c1, c2, c3, c4, c5 = st.columns(
                proporcoes,
                vertical_alignment="center",
            )

            with c1:
                st.markdown(f"**{financeiro.pessoa.nome}**")

            with c2:
                st.write(formatar_cpf(financeiro.pessoa.cpf))

            with c3:
                st.write(financeiro.pessoa.email)

            with c4:
                st.write(
                    financeiro.campus.nome
                    if financeiro.campus
                    else "Não informado"
                )

            with c5:
                visualizar = st.button(
                    ":material/visibility:",
                    key=f"view_financeiro_{financeiro.pessoa_id}",
                    help="Visualizar funcionário",
                    use_container_width=True,
                )

            if visualizar:
                st.session_state["financeiro_id"] = (
                    financeiro.pessoa_id
                )
                from modulos.rotas import view_financeiro_page
                st.switch_page(view_financeiro_page)

            if indice < len(listaFinanceiros) - 1:
                separador()