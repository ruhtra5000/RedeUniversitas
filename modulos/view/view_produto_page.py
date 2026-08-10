import streamlit as st
from modulos.estoque.estoque_service import listarProdutoId
from modulos.utils.view_utils import formatar_situacao_estoque, limpar_consulta_produto
from modulos.utils.view_visual import (CampoBusca, CampoView, SecaoView, renderizarCabecalhoView, renderizarFormularioBusca, renderizarMensagemInicial, renderizarRegistroView)

# Tela de visualização de produto
def telaViewProduto():

    selecionado = st.session_state.pop(
        "produto_selecionado",
        None,
    )

    if selecionado is not None:
        st.session_state["consulta_produto_id"] = selecionado

    produto = None
    erroConsulta = False

    # Função de navegação 
    def voltar():
        from modulos.rotas import (
            listagem_produto_page,
        )

        st.switch_page(listagem_produto_page)

    renderizarCabecalhoView(categoria="View", titulo="Consultar produto", descricao=("Localize um produto utilizando " "o seu identificador."), ao_voltar=voltar, prefixo_chave="produto")

    buscar, valores = renderizarFormularioBusca(
        campos=[
            CampoBusca(
                nome="id",
                rotulo="ID",
                placeholder="Ex.: 1",
                proporcao=1,
                chave="consulta_produto_id_digitado",
            ),
        ],
        prefixo_chave="produto",
        titulo="Localizar produto",
        descricao="Informe o ID do produto.",
    )

    if buscar:
        st.session_state.pop(
            "consulta_produto_id",
            None,
        )

        idProduto = valores["id"].strip()

        if not idProduto:
            st.warning("Informe o ID do produto.")

        elif not idProduto.isdigit():
            st.error("O ID deve conter somente números.")

        else:
            try:
                produto = listarProdutoId(int(idProduto))

                if produto is None:
                    st.error("Produto não encontrado.")

                else:
                    st.session_state["consulta_produto_id"] = produto.id

            except Exception as erro:
                erroConsulta = True
                st.error(str(erro))

    produtoId = st.session_state.get("consulta_produto_id")

    if produto is None and produtoId is not None:
        try:
            produto = listarProdutoId(produtoId)

            if produto is None:
                erroConsulta = True

                st.session_state.pop(
                    "consulta_produto_id",
                    None,
                )

                st.error("Produto não encontrado.")

        except Exception as erro:
            erroConsulta = True

            st.session_state.pop(
                "consulta_produto_id",
                None,
            )

            st.error(str(erro))

    if produto is None:
        if not buscar and not erroConsulta:
            renderizarMensagemInicial("Informe um ID para consultar " "um produto.")

        return

    secoes = [
        SecaoView(
            titulo="Dados do produto",
            descricao=("Identificação e marca do item."),
            linhas=[
                [
                    CampoView(
                        rotulo="ID",
                        valor=lambda item: item.id,
                        proporcao=1,
                    ),
                    CampoView(
                        rotulo="Produto",
                        valor=lambda item: item.nome,
                        proporcao=3,
                    ),
                    CampoView(
                        rotulo="Marca",
                        valor=lambda item: (item.marca or "Não informada"),
                        proporcao=2,
                    ),
                ],
            ],
        ),
        SecaoView(
            titulo="Controle de estoque",
            descricao=("Campus, quantidades e situação atual."),
            linhas=[
                [
                    CampoView(
                        rotulo="Campus",
                        valor=lambda item: (
                            item.campus.nome if item.campus else "Não informado"
                        ),
                        proporcao=2,
                    ),
                    CampoView(
                        rotulo="Quantidade atual",
                        valor=lambda item: item.qtde,
                        proporcao=1,
                        tipo="destaque",
                    ),
                    CampoView(
                        rotulo="Quantidade mínima",
                        valor=lambda item: item.qtde_min,
                        proporcao=1,
                    ),
                ],
                [
                    CampoView(
                        rotulo="Situação",
                        valor=lambda item: (formatar_situacao_estoque(item)),
                        proporcao=1,
                        tipo="badge",
                    ),
                ],
            ],
        ),
    ]

    renderizarRegistroView(
        registro=produto,
        nome=lambda item: item.nome,
        tipo_registro="Produto",
        meta=lambda item: (item.campus.nome if item.campus else "Campus não informado"),
        status=lambda item: (formatar_situacao_estoque(item)),
        secoes=secoes,
        prefixo_chave="produto",
        ao_limpar=limpar_consulta_produto,
        icone="📦",
    )
