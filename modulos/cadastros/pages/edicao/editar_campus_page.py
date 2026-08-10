import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from modulos.academico.academico_service import editarCampus, listarCampusId
from modulos.utils.cadastro_visual import (marcarAcoesCadastro, marcarPainelCadastro, renderizarCabecalhoFormulario, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro, aplicarEstiloCamposBloqueados)

# Tela de edição para Campus
def telaEdicaoCampus():

    aplicarEstiloCamposBloqueados()

    if "ADMIN" not in st.session_state.roles:
        st.error("Acesso negado. Apenas administradores podem " "editar registros.")
        st.stop()

    campus_id = st.session_state.get("edicao_campus_id")

    if not campus_id:
        st.error("Campus não especificado para edição.")

        if st.button("Voltar"):
            from modulos.rotas import view_campus_page

            st.switch_page(view_campus_page)

        st.stop()

    campus = listarCampusId(campus_id)

    if not campus:
        st.error("Campus não encontrado.")
        st.stop()

    if "form_key_edit_campus" not in st.session_state:
        st.session_state.form_key_edit_campus = 0

    # Função para voltar à página de visualização
    def voltarView():
        st.session_state["consulta_campus_id"] = campus_id
        from modulos.rotas import view_campus_page

        st.switch_page(view_campus_page)

    renderizarTopoCadastro(
        titulo="Editar campus",
        descricao="Atualize os dados institucionais da unidade.",
        aoVoltar=voltarView,
        prefixoChave="edicao_campus",
        categoria="EDIÇÃO",
    )

    if st.session_state.pop("edicao_realizada", False):
        st.toast(
            "Dados do campus atualizados com sucesso!",
            icon=":material/check:",
        )

    with st.container(border=True):
        marcarPainelCadastro()

        renderizarCabecalhoFormulario(
            titulo=f"Editando {campus.nome}",
            descricao=(
                "Atualize a identificação e os canais de contato " "da unidade."
            ),
            contexto="EDITANDO REGISTRO",
        )

        renderizarSecaoCadastro(
            numero=1,
            titulo="Dados do campus",
            descricao="Identificação e contato institucional.",
        )

        colNome, colEmail = st.columns(2)

        with colNome:
            nome = st.text_input(
                "Nome do campus *",
                value=campus.nome,
                key=(f"edit_campus_nome_" f"{st.session_state.form_key_edit_campus}"),
            )

        with colEmail:
            email = st.text_input(
                "E-mail de contato *",
                value=campus.email,
                key=(f"edit_campus_email_" f"{st.session_state.form_key_edit_campus}"),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Contato e gestão",
            descricao="Telefone institucional e reitoria designada.",
        )

        colTelefone, colReitor = st.columns(2)

        with colTelefone:
            telefone = st.text_input(
                "Telefone",
                value=campus.telefone or "",
                key=(
                    f"edit_campus_telefone_" f"{st.session_state.form_key_edit_campus}"
                ),
            )

        with colReitor:
            st.text_input(
                "Reitor",
                value=(
                    campus.reitor.pessoa.nome
                    if campus.reitor
                    else "Nenhum reitor designado"
                ),
                disabled=True,
                help=("O reitor é definido através de designação " "de cargo."),
                key=(f"edit_campus_reitor_" f"{st.session_state.form_key_edit_campus}"),
            )

        _, centro, _ = st.columns([2, 3, 2])

        with centro:
            marcarAcoesCadastro()

            salvar = st.button(
                "Salvar alterações",
                icon=":material/save:",
                width="stretch",
                type="primary",
                key=(f"btn_edit_campus_" f"{st.session_state.form_key_edit_campus}"),
            )

    if salvar:
        if not nome.strip() or not email.strip():
            st.error("Preencha todos os campos obrigatórios " "(Nome e E-mail).")

        else:
            try:
                editarCampus(
                    idCampus=campus.id,
                    nome=nome.strip(),
                    email=email.strip(),
                    telefone=(telefone.strip() if telefone.strip() else None),
                )

                st.session_state.form_key_edit_campus += 1
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as erro:
                st.error("Erro ao salvar os dados no banco: " f"{erro}")

            except Exception as erro:
                st.error(str(erro))
