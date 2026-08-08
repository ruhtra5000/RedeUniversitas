import streamlit as st

from modulos.compras.compras_service import listarCompraId
from modulos.utils.view_utils import exibirCampo, formatar_data, formatar_moeda, limpar_consulta_compra, obter_nome_produto, obter_nome_financeiro

# Tela de visualização de compra
def telaViewCompra():

    st.title("🔎 Consulta de Compra")
    st.caption("Pesquise uma compra pelo ID.")

    selecionada = st.session_state.pop("compra_selecionada", None)

    if selecionada is not None:
        st.session_state["consulta_compra_id"] = (
            selecionada
        )

    compra = None
    erro_consulta = False

    col_voltar, _ = st.columns([1, 5])

    with col_voltar:
        if st.button(
            "⬅ Voltar",
            use_container_width=True,
        ):
            pass

    with st.form("buscar_compra", border=True):

        st.markdown("#### 🔍 Buscar compra")

        id_digitado = st.text_input(
            "ID",
            placeholder="Ex.: 1",
            key="consulta_compra_id_digitado",
        )

        coluna_botao, _ = st.columns([1.3, 4.7])

        with coluna_botao:
            buscar = st.form_submit_button(
                "🔍 Buscar",
                type="primary",
                use_container_width=True,
            )

    if buscar:
        st.session_state.pop("consulta_compra_id", None)

        id_compra = id_digitado.strip()

        if not id_compra:
            st.warning("Informe o ID da compra.")

        elif not id_compra.isdigit():
            st.error(
                "O ID deve conter somente números."
            )

        else:
            try:
                compra = listarCompraId(
                    int(id_compra)
                )

                if compra is None:
                    st.error("Compra não encontrada.")

                else:
                    st.session_state[
                        "consulta_compra_id"
                    ] = compra.id

            except Exception as erro:
                erro_consulta = True
                st.error(str(erro))

    compra_id = st.session_state.get(
        "consulta_compra_id"
    )

    if compra is None and compra_id is not None:
        try:
            compra = listarCompraId(compra_id)

            if compra is None:
                erro_consulta = True

                st.session_state.pop("consulta_compra_id", None)

                st.error("Compra não encontrada.")

        except Exception as erro:
            erro_consulta = True

            st.session_state.pop("consulta_compra_id", None)

            st.error(str(erro))

    if compra is None:
        if not buscar and not erro_consulta:
            st.info(
                "Informe um ID para consultar uma compra."
            )

        return

    valor_total = compra.valor_unit * compra.qtde

    st.write("")

    titulo, botao = st.columns(
        [4.7, 1.3],
        vertical_alignment="center",
    )

    with titulo:
        st.subheader(
            f"🛒 Compra de {obter_nome_produto(compra)}"
        )

    with botao:
        st.button(
            "Limpar",
            icon=":material/close:",
            use_container_width=True,
            on_click=limpar_consulta_compra,
        )

    with st.container(border=True):

        st.markdown("#### 🛒 Dados da Compra")

        col1, col2, col3 = st.columns(
            [1, 3, 2]
        )

        altura_dados = 115

        with col1:
            exibirCampo(
                "ID",
                compra.id,
                altura=altura_dados,
            )

        with col2:
            exibirCampo(
                "Produto",
                obter_nome_produto(compra),
                altura=altura_dados,
            )

        with col3:
            exibirCampo(
                "Fornecedor",
                compra.fornecedor.nome
                if compra.fornecedor
                else "Não informado",
                altura=altura_dados,
            )

    st.write("")

    with st.container(border=True):

        st.markdown("#### 💰 Valores")

        col1, col2, col3 = st.columns(3)

        altura_valores = 110

        with col1:
            exibirCampo(
                "Quantidade",
                compra.qtde,
                altura=altura_valores,
            )

        with col2:
            exibirCampo(
                "Valor unitário",
                formatar_moeda(compra.valor_unit),
                altura=altura_valores,
            )

        with col3:
            exibirCampo(
                "Valor total",
                formatar_moeda(valor_total),
                altura=altura_valores,
            )

    st.write("")

    with st.container(border=True):

        st.markdown("#### 📅 Compra e Recebimento")

        col1, col2, col3 = st.columns(3)

        altura_datas = 120

        with col1:
            exibirCampo(
                "Data da compra",
                formatar_data(compra.data_compra),
                altura=altura_datas,
            )

        with col2:
            exibirCampo(
                "Data de recebimento",
                formatar_data(compra.data_recebimento)
                if compra.data_recebimento
                else "Aguardando recebimento",
                altura=altura_datas,
            )

        with col3:
            exibirCampo(
                "Responsável financeiro",
                obter_nome_financeiro(compra),
                altura=altura_datas,
            )