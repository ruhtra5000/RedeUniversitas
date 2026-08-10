import streamlit as st
from modulos.compras.compras_service import listarFornecedorId
from modulos.utils.view_utils import formatar_cnpj, limpar_consulta_fornecedor
from modulos.utils.view_visual import (AcaoView, CampoBusca, CampoView, SecaoView, renderizarCabecalhoView, renderizarFormularioBusca, renderizarMensagemInicial, renderizarRegistroView)

# Tela de visualização de fornecedor
def telaViewFornecedor():

    selecionado = st.session_state.pop(
        "fornecedor_selecionado",
        None,
    )

    if selecionado is not None:
        st.session_state["consulta_fornecedor_id"] = selecionado

    fornecedor = None
    erroConsulta = False

    # Função de navegação 
    def voltar():
        from modulos.rotas import (
            listagem_fornecedor_page,
        )

        st.switch_page(listagem_fornecedor_page)

    renderizarCabecalhoView(categoria="View", titulo="Consultar fornecedor", descricao=("Localize um fornecedor utilizando " "o seu identificador."), ao_voltar=voltar, prefixo_chave="fornecedor")

    buscar, valores = renderizarFormularioBusca(
        campos=[
            CampoBusca(
                nome="id",
                rotulo="ID",
                placeholder="Ex.: 1",
                proporcao=1,
                chave="consulta_fornecedor_id_digitado",
            ),
        ],
        prefixo_chave="fornecedor",
        titulo="Localizar fornecedor",
        descricao="Informe o ID do fornecedor.",
    )

    if buscar:
        st.session_state.pop(
            "consulta_fornecedor_id",
            None,
        )

        idFornecedor = valores["id"].strip()

        if not idFornecedor:
            st.warning("Informe o ID do fornecedor.")

        elif not idFornecedor.isdigit():
            st.error("O ID deve conter somente números.")

        else:
            try:
                fornecedor = listarFornecedorId(int(idFornecedor))

                if fornecedor is None:
                    st.error("Fornecedor não encontrado.")

                else:
                    st.session_state["consulta_fornecedor_id"] = fornecedor.id

            except Exception as erro:
                erroConsulta = True
                st.error(str(erro))

    fornecedorId = st.session_state.get("consulta_fornecedor_id")

    if fornecedor is None and fornecedorId is not None:
        try:
            fornecedor = listarFornecedorId(fornecedorId)

            if fornecedor is None:
                erroConsulta = True

                st.session_state.pop(
                    "consulta_fornecedor_id",
                    None,
                )

                st.error("Fornecedor não encontrado.")

        except Exception as erro:
            erroConsulta = True

            st.session_state.pop(
                "consulta_fornecedor_id",
                None,
            )

            st.error(str(erro))

    if fornecedor is None:
        if not buscar and not erroConsulta:
            renderizarMensagemInicial("Informe um ID para consultar " "um fornecedor.")

        return

    # Função para edição de fornecedor
    def editar(registro):
        st.session_state["edicao_fornecedor_id"] = registro.id

        from modulos.rotas import (
            editar_fornecedor_page,
        )

        st.switch_page(editar_fornecedor_page)

    acoes = []

    if "ADMIN" in st.session_state.get("roles", []):
        acoes.append(
            AcaoView(
                rotulo="Editar",
                icone=":material/edit:",
                tipo="secondary",
                chave="editar",
                ao_clicar=editar,
            )
        )

    secoes = [
        SecaoView(
            titulo="Dados do fornecedor",
            descricao=("Identificação da empresa fornecedora."),
            linhas=[
                [
                    CampoView(
                        rotulo="ID",
                        valor=lambda item: item.id,
                        proporcao=1,
                    ),
                    CampoView(
                        rotulo="Fornecedor",
                        valor=lambda item: item.nome,
                        proporcao=3,
                    ),
                    CampoView(
                        rotulo="CNPJ",
                        valor=lambda item: formatar_cnpj(item.cnpj),
                        proporcao=2,
                    ),
                ],
            ],
        ),
        SecaoView(
            titulo="Informações de contato",
            descricao=("Canais de comunicação do fornecedor."),
            linhas=[
                [
                    CampoView(
                        rotulo="E-mail",
                        valor=lambda item: (item.email or "Não informado"),
                        proporcao=1,
                        tipo="email",
                    ),
                    CampoView(
                        rotulo="Telefone",
                        valor=lambda item: (item.telefone or "Não informado"),
                        proporcao=1,
                    ),
                ],
            ],
        ),
    ]

    renderizarRegistroView(
        registro=fornecedor,
        nome=lambda item: item.nome,
        tipo_registro="Fornecedor",
        meta=lambda item: formatar_cnpj(item.cnpj),
        status="Registro localizado",
        secoes=secoes,
        prefixo_chave="fornecedor",
        ao_limpar=limpar_consulta_fornecedor,
        acoes=acoes,
    )
