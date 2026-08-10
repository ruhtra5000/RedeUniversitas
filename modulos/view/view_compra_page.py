import streamlit as st
from modulos.compras.compras_service import listarCompraId
from modulos.utils.view_utils import (formatar_data, formatar_moeda, limpar_consulta_compra, obter_nome_financeiro, obter_nome_produto)
from modulos.utils.view_visual import (CampoBusca, CampoView, SecaoView, renderizarCabecalhoView, renderizarFormularioBusca, renderizarMensagemInicial, renderizarRegistroView)

# Tela de visualização de compra
def telaViewCompra():

    selecionada = st.session_state.pop(
        "compra_selecionada",
        None,
    )

    if selecionada is not None:
        st.session_state["consulta_compra_id"] = selecionada

    compra = None
    erroConsulta = False

    # Função de navegação 
    def voltar():
        from modulos.rotas import listagem_compra_page

        st.switch_page(listagem_compra_page)

    renderizarCabecalhoView(categoria="View", titulo="Consultar compra", descricao=("Localize uma compra utilizando " "o seu identificador."), ao_voltar=voltar, prefixo_chave="compra")

    buscar, valores = renderizarFormularioBusca(
        campos=[
            CampoBusca(
                nome="id",
                rotulo="ID",
                placeholder="Ex.: 1",
                proporcao=1,
                chave="consulta_compra_id_digitado",
            ),
        ],
        prefixo_chave="compra",
        titulo="Localizar compra",
        descricao="Informe o ID da compra.",
    )

    if buscar:
        st.session_state.pop("consulta_compra_id", None)

        idCompra = valores["id"].strip()

        if not idCompra:
            st.warning("Informe o ID da compra.")

        elif not idCompra.isdigit():
            st.error("O ID deve conter somente números.")

        else:
            try:
                compra = listarCompraId(int(idCompra))

                if compra is None:
                    st.error("Compra não encontrada.")

                else:
                    st.session_state["consulta_compra_id"] = compra.id

            except Exception as erro:
                erroConsulta = True
                st.error(str(erro))

    compraId = st.session_state.get("consulta_compra_id")

    if compra is None and compraId is not None:
        try:
            compra = listarCompraId(compraId)

            if compra is None:
                erroConsulta = True

                st.session_state.pop(
                    "consulta_compra_id",
                    None,
                )

                st.error("Compra não encontrada.")

        except Exception as erro:
            erroConsulta = True

            st.session_state.pop(
                "consulta_compra_id",
                None,
            )

            st.error(str(erro))

    if compra is None:
        if not buscar and not erroConsulta:
            renderizarMensagemInicial("Informe um ID para consultar uma compra.")

        return

    valorTotal = compra.valor_unit * compra.qtde

    secoes = [
        SecaoView(
            titulo="Dados da compra",
            descricao=("Produto e fornecedor vinculados " "à aquisição."),
            linhas=[
                [
                    CampoView(
                        rotulo="ID",
                        valor=lambda item: item.id,
                        proporcao=1,
                    ),
                    CampoView(
                        rotulo="Produto",
                        valor=obter_nome_produto,
                        proporcao=3,
                    ),
                    CampoView(
                        rotulo="Fornecedor",
                        valor=lambda item: (
                            item.fornecedor.nome if item.fornecedor else "Não informado"
                        ),
                        proporcao=2,
                    ),
                ],
            ],
        ),
        SecaoView(
            titulo="Valores",
            descricao=("Quantidade e valores da compra."),
            linhas=[
                [
                    CampoView(
                        rotulo="Quantidade",
                        valor=lambda item: item.qtde,
                        proporcao=1,
                    ),
                    CampoView(
                        rotulo="Valor unitário",
                        valor=lambda item: formatar_moeda(item.valor_unit),
                        proporcao=1,
                    ),
                    CampoView(
                        rotulo="Valor total",
                        valor=lambda item: formatar_moeda(valorTotal),
                        proporcao=1,
                        tipo="destaque",
                    ),
                ],
            ],
        ),
        SecaoView(
            titulo="Compra e recebimento",
            descricao=("Datas e responsável financeiro."),
            linhas=[
                [
                    CampoView(
                        rotulo="Data da compra",
                        valor=lambda item: formatar_data(item.data_compra),
                        proporcao=1,
                    ),
                    CampoView(
                        rotulo="Data de recebimento",
                        valor=lambda item: (
                            formatar_data(item.data_recebimento)
                            if item.data_recebimento
                            else "Aguardando recebimento"
                        ),
                        proporcao=1,
                        tipo="badge",
                    ),
                    CampoView(
                        rotulo="Responsável financeiro",
                        valor=obter_nome_financeiro,
                        proporcao=1,
                    ),
                ],
            ],
        ),
    ]

    renderizarRegistroView(
        registro=compra,
        nome=lambda item: (f"Compra de {obter_nome_produto(item)}"),
        tipo_registro="Compra",
        meta=lambda item: (
            item.fornecedor.nome if item.fornecedor else "Fornecedor não informado"
        ),
        status=lambda item: (
            "Recebida" if item.data_recebimento else "Aguardando recebimento"
        ),
        secoes=secoes,
        prefixo_chave="compra",
        ao_limpar=limpar_consulta_compra,
    )
