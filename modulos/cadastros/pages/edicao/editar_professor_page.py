import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from modulos.academico.academico_service import editarPessoa, listarProfessorId
from modulos.utils.cadastro_visual import (marcarAcoesCadastro, marcarPainelCadastro, renderizarCabecalhoFormulario, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro, aplicarEstiloCamposBloqueados)

# Tela de edição para Professores
def telaEdicaoProfessor():

    aplicarEstiloCamposBloqueados()

    if "ADMIN" not in st.session_state.roles:
        st.error("Acesso negado. Apenas administradores podem " "editar registros.")
        st.stop()

    professor_id = st.session_state.get("edicao_professor_id")

    if not professor_id:
        st.error("Professor não especificado para edição.")

        if st.button("Voltar"):
            from modulos.rotas import view_professor_page

            st.switch_page(view_professor_page)

        st.stop()

    professor = listarProfessorId(professor_id)

    if not professor:
        st.error("Professor não encontrado.")
        st.stop()

    if "form_key_edit_professor" not in st.session_state:
        st.session_state.form_key_edit_professor = 0

    # Função para voltar à página de visualização
    def voltarView():
        st.session_state["consulta_professor_id"] = professor_id
        from modulos.rotas import view_professor_page

        st.switch_page(view_professor_page)

    renderizarTopoCadastro(
        titulo="Editar professor",
        descricao="Atualize os dados pessoais e de contato do professor.",
        aoVoltar=voltarView,
        prefixoChave="edicao_professor",
        categoria="EDIÇÃO",
    )

    if st.session_state.pop("edicao_realizada", False):
        st.toast(
            "Dados do professor atualizados com sucesso!",
            icon=":material/check:",
        )

    with st.container(border=True):
        marcarPainelCadastro()

        renderizarCabecalhoFormulario(
            titulo=f"Editando {professor.pessoa.nome}",
            descricao=(
                "Mantenha os dados de identificação e contato do "
                "docente atualizados."
            ),
            contexto="EDITANDO REGISTRO",
        )

        renderizarSecaoCadastro(
            numero=1,
            titulo="Dados pessoais",
            descricao="Identificação e canais de contato do professor.",
        )

        colNome, colEmail = st.columns(2)

        with colNome:
            nome = st.text_input(
                "Nome completo *",
                value=professor.pessoa.nome,
                key=(
                    f"edit_professor_nome_"
                    f"{st.session_state.form_key_edit_professor}"
                ),
            )

        with colEmail:
            email = st.text_input(
                "E-mail *",
                value=professor.pessoa.email,
                key=(
                    f"edit_professor_email_"
                    f"{st.session_state.form_key_edit_professor}"
                ),
            )

        colCpf, colTelefone = st.columns(2)

        with colCpf:
            st.text_input(
                "CPF",
                value=professor.pessoa.cpf,
                disabled=True,
                help="O CPF não pode ser alterado nesta tela.",
                key=(
                    f"edit_professor_cpf_" f"{st.session_state.form_key_edit_professor}"
                ),
            )

        with colTelefone:
            telefone = st.text_input(
                "Telefone",
                value=professor.pessoa.telefone or "",
                key=(
                    f"edit_professor_telefone_"
                    f"{st.session_state.form_key_edit_professor}"
                ),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Vínculo institucional",
            descricao="Unidade acadêmica à qual o professor está vinculado.",
        )

        st.text_input(
            "Campus",
            value=professor.campus.nome if professor.campus else "",
            disabled=True,
            help="O campus do professor não pode ser alterado diretamente.",
            key=(
                f"edit_professor_campus_" f"{st.session_state.form_key_edit_professor}"
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
                    f"btn_edit_professor_" f"{st.session_state.form_key_edit_professor}"
                ),
            )

    if salvar:
        if not nome.strip() or not email.strip():
            st.error("Preencha todos os campos obrigatórios " "(Nome e E-mail).")

        else:
            try:
                editarPessoa(
                    idPessoa=professor.pessoa_id,
                    nome=nome.strip(),
                    email=email.strip(),
                    telefone=(telefone.strip() if telefone.strip() else None),
                )

                st.session_state.form_key_edit_professor += 1
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as erro:
                st.error("Erro ao salvar os dados no banco: " f"{erro}")

            except Exception as erro:
                st.error(str(erro))
