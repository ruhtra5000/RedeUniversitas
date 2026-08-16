import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from modulos.academico.academico_service import editarPessoa, listarAlunoId, alterarStatusAluno
from modulos.utils.cadastro_visual import (marcarAcoesCadastro, marcarPainelCadastro, renderizarCabecalhoFormulario, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro, aplicarEstiloCamposBloqueados)
from database.entidades.enums.StatusAluno import StatusAluno

# Tela de edição para Alunos
def telaEdicaoAluno():

    aplicarEstiloCamposBloqueados()

    if "ADMIN" not in st.session_state.roles:
        st.error("Acesso negado. Apenas administradores podem " "editar registros.")
        st.stop()

    aluno_id = st.session_state.get("edicao_aluno_id")

    if not aluno_id:
        st.error("Aluno não especificado para edição.")

        if st.button("Voltar"):
            from modulos.rotas import view_aluno_page

            st.switch_page(view_aluno_page)

        st.stop()

    aluno = listarAlunoId(aluno_id)

    if not aluno:
        st.error("Aluno não encontrado.")
        st.stop()

    if "form_key_edit_aluno" not in st.session_state:
        st.session_state.form_key_edit_aluno = 0

    # Função para voltar à página de visualização
    def voltarView():
        st.session_state["consulta_aluno_id"] = aluno_id
        from modulos.rotas import view_aluno_page

        st.switch_page(view_aluno_page)

    renderizarTopoCadastro(
        titulo="Editar aluno",
        descricao="Atualize os dados pessoais do estudante.",
        aoVoltar=voltarView,
        prefixoChave="edicao_aluno",
        categoria="EDIÇÃO",
    )

    if st.session_state.pop("edicao_realizada", False):
        st.toast(
            "Dados do aluno atualizados com sucesso!",
            icon=":material/check:",
        )

    with st.container(border=True):
        marcarPainelCadastro()

        renderizarCabecalhoFormulario(
            titulo=f"Editando {aluno.pessoa.nome}",
            descricao=(
                "Altere as informações permitidas e consulte o "
                "vínculo acadêmico atual."
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
                value=aluno.pessoa.nome,
                key=(f"edit_aluno_nome_" f"{st.session_state.form_key_edit_aluno}"),
            )

        with colEmail:
            email = st.text_input(
                "E-mail *",
                value=aluno.pessoa.email,
                key=(f"edit_aluno_email_" f"{st.session_state.form_key_edit_aluno}"),
            )

        colCpf, colTelefone = st.columns(2)

        with colCpf:
            cpf = st.text_input(
                "CPF (somente leitura)",
                value=aluno.pessoa.cpf,
                disabled=True,
                key=(f"edit_aluno_cpf_" f"{st.session_state.form_key_edit_aluno}"),
            )

        with colTelefone:
            telefone = st.text_input(
                "Telefone",
                value=aluno.pessoa.telefone or "",
                key=(f"edit_aluno_telefone_" f"{st.session_state.form_key_edit_aluno}"),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Dados acadêmicos",
            descricao="Campus e curso atuais do estudante.",
        )

        status_atual = aluno.status or StatusAluno.ATIVO
        opcoes_status = list(StatusAluno)

        colCampus, colCurso, colStatus = st.columns([2, 2, 1.5])

        with colCampus:
            st.text_input(
                "Campus",
                value=aluno.campus.nome if aluno.campus else "",
                disabled=True,
                help="O campus do aluno não pode ser alterado diretamente.",
                key=(
                    f"edit_aluno_campus_"
                    f"{st.session_state.form_key_edit_aluno}"
                ),
            )

        with colCurso:
            st.text_input(
                "Curso",
                value=aluno.curso.nome if aluno.curso else "",
                disabled=True,
                help="O curso do aluno não pode ser alterado diretamente.",
                key=(
                    f"edit_aluno_curso_"
                    f"{st.session_state.form_key_edit_aluno}"
                ),
            )

        with colStatus:
            novoStatus = st.selectbox(
                "Status acadêmico *",
                options=opcoes_status,
                index=opcoes_status.index(status_atual),
                format_func=lambda status: status.value.replace("_", " ").title(),
                key=(
                    f"edit_aluno_status_"
                    f"{st.session_state.form_key_edit_aluno}"
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
                key=(f"btn_edit_aluno_" f"{st.session_state.form_key_edit_aluno}"),
            )

    if salvar:
        if not nome.strip() or not email.strip():
            st.error("Preencha todos os campos obrigatórios " "(Nome e E-mail).")

        else:
            try:
                editarPessoa(
                    idPessoa=aluno.pessoa_id,
                    nome=nome.strip(),
                    email=email.strip(),
                    telefone=(telefone.strip() if telefone.strip() else None),
                )

                alterarStatusAluno(idAluno=aluno.pessoa_id, novoStatus=novoStatus)
                st.session_state.pop("cache_alunos", None)

                st.session_state.form_key_edit_aluno += 1
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as erro:
                st.error("Erro ao salvar os dados no banco: " f"{erro}")

            except Exception as erro:
                st.error(str(erro))
