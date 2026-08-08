import streamlit as st
from modulos.academico.academico_service import listarBolsasGeral
from modulos.utils.listagem_utils import separador, formatar_percentual, formatar_data, formatar_status

# Tela de listagem de bolsas
def telaListagemBolsas():

    st.title(":material/assignment: Listagem de Bolsas")
    st.caption("Consulte as bolsas cadastradas no sistema.")


    listaBolsas = listarBolsasGeral()

    if not listaBolsas:
        st.info(":material/school: Nenhuma bolsa cadastrada.")
        return

    st.write("")

    st.caption(
        f":material/school: {len(listaBolsas)} "
        f"{'bolsa encontrada' if len(listaBolsas) == 1 else 'bolsas encontradas'}"
    )

    proporcoes = [3, 2.2, 2, 2, 2.5, 1.3]

    with st.container(border=True):

        h1, h2, h3, h4, h5, h6 = st.columns(
            proporcoes,
            vertical_alignment="center",
        )

        h1.markdown("**Aluno**")
        h2.markdown("**Tipo**")
        h3.markdown("**Desconto**")
        h4.markdown("**Início**")
        h5.markdown("**Status**")
        h6.markdown("**Ações**")

        separador()

        for indice, bolsa in enumerate(listaBolsas):

            c1, c2, c3, c4, c5, c6 = st.columns(
                proporcoes,
                vertical_alignment="center",
            )

            with c1:
                st.markdown(f"**{bolsa.aluno.pessoa.nome}**")

            with c2:
                st.write(bolsa.tipo_bolsa)

            with c3:
                st.write(
                    formatar_percentual(
                        bolsa.percentual_desconto
                    )
                )

            with c4:
                st.write(formatar_data(bolsa.data_inicio))

            with c5:
                st.write(formatar_status(bolsa.status))

            with c6:
                visualizar = st.button(
                    ":material/visibility:",
                    key=f"view_bolsa_{bolsa.id}",
                    help="Visualizar bolsa",
                    use_container_width=True,
                )

            if visualizar:
                st.session_state["bolsa_id"] = bolsa.id

                st.rerun()

            if indice < len(listaBolsas) - 1:
                separador()