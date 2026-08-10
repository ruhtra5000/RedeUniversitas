import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from database.entidades.Estoque import Estoque
from modulos.academico.academico_service import listarCampus
from modulos.cadastros.estoque import criarEstoque
from modulos.utils.cadastro_visual import (painelCadastro, renderizarAvisoCadastro, renderizarBotaoCadastro, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro)

# Tela de cadastro para Produtos no Estoque
def telaCadastroEstoque():
    if "form_key_estoque" not in st.session_state:
        st.session_state.form_key_estoque = 0

    # Função para voltar à página de cadastros
    def voltarCadastros():
        from modulos.rotas import cadastros_page

        st.switch_page(cadastros_page)

    renderizarTopoCadastro(
        titulo="Cadastrar produto",
        descricao=(
            "Adicione um novo item ao estoque e configure " "seus níveis de controle."
        ),
        aoVoltar=voltarCadastros,
        prefixoChave="cadastro_produto",
    )

    if st.session_state.pop("cadastro_estoque_realizado", False):
        st.toast(
            "Produto cadastrado com sucesso!",
            icon=":material/check:",
        )

    if "cache_campus" not in st.session_state:
        st.session_state.cache_campus = listarCampus()

    lista_campus = st.session_state.cache_campus

    if not lista_campus:
        renderizarAvisoCadastro(
            titulo="Campus necessário",
            descricao=(
                "Cadastre pelo menos um campus antes de adicionar "
                "um produto ao estoque."
            ),
        )

    with painelCadastro(
        titulo="Informações do produto",
        descricao=(
            "Defina a identificação, o local de armazenamento "
            "e as quantidades de controle."
        ),
    ):

        renderizarSecaoCadastro(
            numero=1,
            titulo="Dados do produto",
            descricao="Nome comercial e marca do item.",
        )

        colNome, colMarca = st.columns(2)

        with colNome:
            nome = st.text_input(
                "Nome do produto *",
                placeholder="Ex.: Resma de Papel A4",
                key=(f"est_nome_" f"{st.session_state.form_key_estoque}"),
            )

        with colMarca:
            marca = st.text_input(
                "Marca *",
                placeholder="Ex.: Chamex",
                key=(f"est_marca_" f"{st.session_state.form_key_estoque}"),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Alocação e controle",
            descricao="Campus responsável e limites do estoque.",
        )

        campus_selecionado = st.selectbox(
            "Campus de alocação *",
            options=lista_campus if lista_campus else [],
            format_func=lambda item: item.nome,
            index=None,
            placeholder="Selecione um campus...",
            disabled=not lista_campus,
            key=(f"est_campus_" f"{st.session_state.form_key_estoque}"),
        )

        colQuantidade, colMinimo = st.columns(2)

        with colQuantidade:
            qtde = st.number_input(
                "Quantidade atual",
                min_value=0,
                value=0,
                step=1,
                help=(
                    "Quantidade do produto que já se encontra " "em estoque, se houver."
                ),
                key=(f"est_qtde_" f"{st.session_state.form_key_estoque}"),
            )

        with colMinimo:
            qtde_min = st.number_input(
                "Quantidade mínima *",
                min_value=0,
                value=0,
                step=1,
                help=(
                    "Quantidade mínima recomendada para acionar "
                    "um alerta de reposição."
                ),
                key=(f"est_qtde_min_" f"{st.session_state.form_key_estoque}"),
            )

        cadastrar = renderizarBotaoCadastro(
            rotulo="Cadastrar produto",
            icone=":material/inventory_2:",
            chave=(f"btn_cad_estoque_" f"{st.session_state.form_key_estoque}"),
        )

    if cadastrar:
        if not lista_campus:
            st.error("Cadastre pelo menos um Campus antes de continuar.")

        elif not nome.strip() or not marca.strip():
            st.error("Por favor, preencha os campos obrigatórios " "(Nome e Marca).")

        elif campus_selecionado is None:
            st.error("Por favor, selecione um Campus.")

        else:
            try:
                novo_produto = Estoque(
                    nome=nome.strip(),
                    marca=marca.strip(),
                    qtde=qtde,
                    qtde_min=qtde_min,
                    campus_id=campus_selecionado.id,
                )

                criarEstoque(produto=novo_produto)

                st.session_state.form_key_estoque += 1
                st.session_state.pop("cache_produtos", None)
                st.session_state["cadastro_estoque_realizado"] = True

                st.rerun()

            except SQLAlchemyError as erro:
                st.error("Erro ao salvar os dados no banco: " f"{erro}")

            except Exception as erro:
                st.error(str(erro))
