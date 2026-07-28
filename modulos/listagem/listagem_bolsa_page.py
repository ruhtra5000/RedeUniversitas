import streamlit as st

from modulos.academico.academico_db import dbListarBolsasGeral
from modulos.utils.listagem_utils import separador

# Função para formatar o percentual de desconto da bolsa
def formatarPercentual(valor):
    if valor is None:
        return "Não informado"

    return f"{float(valor) * 100:.0f}%"

# Função para formatar a data de início da bolsa
def formatarData(data):
    if data is None:
        return "Não informada"

    return data.strftime("%d/%m/%Y")

# Função para formatar o status da bolsa
def formatarStatus(status):
    if status is None:
        return "Não informado"

    valor = status.value if hasattr(status, "value") else str(status)

    return str(valor).replace("_", " ").title()

# Tela de listagem de bolsas
def telaListagemBolsas():

    st.title("📋 Listagem de Bolsas")
    st.caption("Consulte as bolsas cadastradas no sistema.")

    colVoltar, _ = st.columns([1, 5])

    with colVoltar:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import home_page
            st.switch_page(home_page)

    listaBolsas = dbListarBolsasGeral()

    if not listaBolsas:
        st.info("🎓 Nenhuma bolsa cadastrada.")
        return

    st.write("")

    st.caption(
        f"🎓 {len(listaBolsas)} "
        f"{'bolsa encontrada' if len(listaBolsas) == 1 else 'bolsas encontradas'}"
    )

    proporcoes = [3, 2.2, 3.2, 2.5, 1.3]

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
                    formatarPercentual(
                        bolsa.percentual_desconto
                    )
                )

            with c4:
                st.write(formatarData(bolsa.data_inicio))

            with c5:
                st.write(formatarStatus(bolsa.status))

            with c6:
                visualizar = st.button(
                    "👁️",
                    key=f"view_bolsa_{bolsa.id}",
                    help="Visualizar bolsa",
                    use_container_width=True,
                )

            if visualizar:
                st.session_state["bolsa_id"] = bolsa.id

                from modulos.rotas import view_bolsa_page
                st.switch_page(view_bolsa_page)

            if indice < len(listaBolsas) - 1:
                separador()