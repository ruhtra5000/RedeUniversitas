import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from modulos.academico.academico_service import editarPessoa
from modulos.estoque.estoque_service import listarAlmoxarifeId
from modulos.utils.cadastro_visual import (marcarAcoesCadastro, marcarPainelCadastro, renderizarCabecalhoFormulario, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro, aplicarEstiloCamposBloqueados)

# Tela de edição para Almoxarifes
def telaEdicaoAlmoxarife():

    aplicarEstiloCamposBloqueados()

    if "ADMIN" not in st.session_state.roles:
        st.error("Acesso negado. Apenas administradores podem " "editar registros.")
        st.stop()

    almoxarife_id = st.session_state.get("edicao_almoxarife_id")

    if not almoxarife_id:
        st.error("Almoxarife não especificado para edição.")

        if st.button("Voltar"):
            from modulos.rotas import view_almoxarife_page

            st.switch_page(view_almoxarife_page)

        st.stop()

    almoxarife = listarAlmoxarifeId(almoxarife_id)

    if not almoxarife:
        st.error("Almoxarife não encontrado.")
        st.stop()

    if "form_key_edit_almoxarife" not in st.session_state:
        st.session_state.form_key_edit_almoxarife = 0

    # Função para voltar à página de visualização
    def voltarView():
        st.session_state["consulta_almoxarife_id"] = almoxarife_id
        from modulos.rotas import view_almoxarife_page

        st.switch_page(view_almoxarife_page)

    renderizarTopoCadastro(
        titulo="Editar almoxarife",
        descricao="Atualize os dados pessoais do profissional.",
        aoVoltar=voltarView,
        prefixoChave="edicao_almoxarife",
        categoria="EDIÇÃO",
    )

    if st.session_state.pop("edicao_realizada", False):
        st.toast(
            "Dados do almoxarife atualizados com sucesso!",
            icon=":material/check:",
        )

    with st.container(border=True):
        marcarPainelCadastro()

        renderizarCabecalhoFormulario(
            titulo=f"Editando {almoxarife.pessoa.nome}",
            descricao=(
                "Altere as informações permitidas e revise os "
                "dados institucionais somente para consulta."
            ),
            contexto="EDITANDO REGISTRO",
        )

        renderizarSecaoCadastro(
            numero=1,
            titulo="Dados pessoais",
            descricao="Informações de identificação e contato.",
        )

        colNome, colEmail = st.columns(2)

        with colNome:
            nome = st.text_input(
                "Nome completo *",
                value=almoxarife.pessoa.nome,
                key=(
                    f"edit_almoxarife_nome_"
                    f"{st.session_state.form_key_edit_almoxarife}"
                ),
            )

        with colEmail:
            email = st.text_input(
                "E-mail *",
                value=almoxarife.pessoa.email,
                key=(
                    f"edit_almoxarife_email_"
                    f"{st.session_state.form_key_edit_almoxarife}"
                ),
            )

        colCpf, colTelefone = st.columns(2)

        with colCpf:
            cpf = st.text_input(
                "CPF (somente leitura)",
                value=almoxarife.pessoa.cpf,
                disabled=True,
                key=(
                    f"edit_almoxarife_cpf_"
                    f"{st.session_state.form_key_edit_almoxarife}"
                ),
            )

        with colTelefone:
            telefone = st.text_input(
                "Telefone",
                value=almoxarife.pessoa.telefone or "",
                key=(
                    f"edit_almoxarife_telefone_"
                    f"{st.session_state.form_key_edit_almoxarife}"
                ),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Vínculo institucional",
            descricao="Campus atualmente associado ao profissional.",
        )

        st.text_input(
            "Campus",
            value=(almoxarife.campus.nome if almoxarife.campus else ""),
            disabled=True,
            help=("O campus do almoxarife não pode ser alterado " "diretamente."),
            key=(
                f"edit_almoxarife_campus_"
                f"{st.session_state.form_key_edit_almoxarife}"
            ),
        )

        _, centro, _ = st.columns([2, 3, 2])

        with centro:
            marcarAcoesCadastro()

            salvar = st.button(
                "Salvar alterações",
                icon=":material/save:",
                width="stretch",
                type="primary",
                key=(
                    f"btn_edit_almoxarife_"
                    f"{st.session_state.form_key_edit_almoxarife}"
                ),
            )

    if salvar:
        if not nome.strip() or not email.strip():
            st.error("Preencha todos os campos obrigatórios " "(Nome e E-mail).")

        else:
            try:
                editarPessoa(
                    idPessoa=almoxarife.pessoa_id,
                    nome=nome.strip(),
                    email=email.strip(),
                    telefone=(telefone.strip() if telefone.strip() else None),
                )

                st.session_state.form_key_edit_almoxarife += 1
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as erro:
                st.error("Erro ao salvar os dados no banco: " f"{erro}")

            except Exception as erro:
                st.error(str(erro))
