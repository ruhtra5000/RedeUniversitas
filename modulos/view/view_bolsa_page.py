import streamlit as st
from modulos.academico.academico_service import listarBolsaId
from modulos.utils.view_utils import formatar_percentual, formatar_data, formatar_status, exibirCampo, limpar_consulta_bolsa

# Tela de visualização de bolsa
def telaViewBolsa():

    st.title("🔎 Consulta de Bolsa")
    st.caption("Pesquise uma bolsa pelo ID.")

    if "bolsa_id" in st.session_state:
        st.session_state["consulta_bolsa_id"] = (
            st.session_state.pop("bolsa_id")
        )

    bolsa = None

    colVoltar, _ = st.columns([1, 5])

    with colVoltar:
        if st.button("⬅ Voltar", use_container_width=True):
            pass

    with st.form("buscar_bolsa", border=True):

        st.markdown("#### 🔍 Buscar bolsa")

        idDigitado = st.text_input(
            "ID da bolsa",
            placeholder="Ex.: 1",
            key="consulta_bolsa_id_digitado",
        )

        colunaBotao, _ = st.columns([1.3, 4.7])

        with colunaBotao:
            buscar = st.form_submit_button(
                "🔍 Buscar",
                type="primary",
                use_container_width=True,
            )

    if buscar:
        st.session_state.pop("consulta_bolsa_id", None)

        idBolsa = idDigitado.strip()

        if not idBolsa:
            st.warning("Informe o ID da bolsa.")

        elif not idBolsa.isdigit():
            st.error("O ID deve conter somente números.")

        else:
            bolsa = listarBolsaId(int(idBolsa))

            if bolsa is None:
                st.error("Bolsa não encontrada.")
            else:
                st.session_state["consulta_bolsa_id"] = bolsa.id

    idBolsa = st.session_state.get("consulta_bolsa_id")

    if bolsa is None and idBolsa is not None:
        bolsa = listarBolsaId(idBolsa)

    if bolsa is None:
        if not buscar:
            st.info("Informe o ID para consultar uma bolsa.")

        return

    st.write("")

    titulo, botao = st.columns(
        [4.7, 1.3],
        vertical_alignment="center",
    )

    with titulo:
        st.subheader(f"🎓 Bolsa #{bolsa.id}")

    with botao:
        st.button(
            "Limpar",
            icon=":material/close:",
            use_container_width=True,
            on_click=limpar_consulta_bolsa,
        )

    with st.container(border=True):

        st.markdown("#### 👤 Aluno")

        col1, col2, col3 = st.columns([1, 3, 2])

        with col1:
            exibirCampo("ID da bolsa", bolsa.id)

        with col2:
            exibirCampo("Aluno", bolsa.aluno.pessoa.nome)

        with col3:
            exibirCampo("Matrícula", bolsa.aluno.matricula)

    st.write("")

    with st.container(border=True):

        st.markdown("#### 🎓 Dados da Bolsa")

        col1, col2, col3 = st.columns(3)

        with col1:
            exibirCampo("Tipo", bolsa.tipo_bolsa)

        with col2:
            exibirCampo(
                "Desconto",
                formatar_percentual(
                    bolsa.percentual_desconto
                ),
            )

        with col3:
            exibirCampo(
                "Status",
                formatar_status(bolsa.status),
            )

        st.write("")

        col1, col2 = st.columns(2)

        with col1:
            exibirCampo(
                "Data de início",
                formatar_data(bolsa.data_inicio),
            )

        with col2:
            exibirCampo(
                "Data de término",
                formatar_data(bolsa.data_fim),
            )