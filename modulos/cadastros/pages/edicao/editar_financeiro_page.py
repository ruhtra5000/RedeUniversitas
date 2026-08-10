import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from modulos.academico.academico_service import editarPessoa
from modulos.financeiro.financeiro_service import listarFinanceiroId
from modulos.utils.cadastro_visual import (marcarAcoesCadastro, marcarPainelCadastro, renderizarCabecalhoFormulario, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro, aplicarEstiloCamposBloqueados)

# Tela de edição para membros do financeiro
def telaEdicaoFinanceiro():

    aplicarEstiloCamposBloqueados()

    if "ADMIN" not in st.session_state.roles:
        st.error("Acesso negado. Apenas administradores podem " "editar registros.")
        st.stop()

    financeiro_id = st.session_state.get("edicao_financeiro_id")

    if not financeiro_id:
        st.error("Membro do financeiro não especificado para edição.")

        if st.button("Voltar"):
            from modulos.rotas import view_financeiro_page

            st.switch_page(view_financeiro_page)

        st.stop()

    financeiro = listarFinanceiroId(financeiro_id)

    if not financeiro:
        st.error("Membro do financeiro não encontrado.")
        st.stop()

    if "form_key_edit_financeiro" not in st.session_state:
        st.session_state.form_key_edit_financeiro = 0

    # Função para voltar à página de visualização
    def voltarView():
        st.session_state["consulta_financeiro_id"] = financeiro_id
        from modulos.rotas import view_financeiro_page

        st.switch_page(view_financeiro_page)

    renderizarTopoCadastro(
        titulo="Editar financeiro",
        descricao="Atualize os dados pessoais do membro do financeiro.",
        aoVoltar=voltarView,
        prefixoChave="edicao_financeiro",
        categoria="EDIÇÃO",
    )

    if st.session_state.pop("edicao_realizada", False):
        st.toast(
            "Dados do financeiro atualizados com sucesso!",
            icon=":material/check:",
        )

    with st.container(border=True):
        marcarPainelCadastro()

        renderizarCabecalhoFormulario(
            titulo=f"Editando {financeiro.pessoa.nome}",
            descricao=(
                "Mantenha os dados de contato atualizados para o "
                "atendimento financeiro."
            ),
            contexto="EDITANDO REGISTRO",
        )

        renderizarSecaoCadastro(
            numero=1,
            titulo="Dados pessoais",
            descricao="Identificação e canais de contato do profissional.",
        )

        colNome, colEmail = st.columns(2)

        with colNome:
            nome = st.text_input(
                "Nome completo *",
                value=financeiro.pessoa.nome,
                key=(
                    f"edit_financeiro_nome_"
                    f"{st.session_state.form_key_edit_financeiro}"
                ),
            )

        with colEmail:
            email = st.text_input(
                "E-mail *",
                value=financeiro.pessoa.email,
                key=(
                    f"edit_financeiro_email_"
                    f"{st.session_state.form_key_edit_financeiro}"
                ),
            )

        colCpf, colTelefone = st.columns(2)

        with colCpf:
            st.text_input(
                "CPF",
                value=financeiro.pessoa.cpf,
                disabled=True,
                help="O CPF não pode ser alterado nesta tela.",
                key=(
                    f"edit_financeiro_cpf_"
                    f"{st.session_state.form_key_edit_financeiro}"
                ),
            )

        with colTelefone:
            telefone = st.text_input(
                "Telefone",
                value=financeiro.pessoa.telefone or "",
                key=(
                    f"edit_financeiro_telefone_"
                    f"{st.session_state.form_key_edit_financeiro}"
                ),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Vínculo institucional",
            descricao="Unidade à qual o profissional está vinculado.",
        )

        st.text_input(
            "Campus",
            value=financeiro.campus.nome if financeiro.campus else "",
            disabled=True,
            help="O campus não pode ser alterado diretamente.",
            key=(
                f"edit_financeiro_campus_"
                f"{st.session_state.form_key_edit_financeiro}"
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
                    f"btn_edit_financeiro_"
                    f"{st.session_state.form_key_edit_financeiro}"
                ),
            )

    if salvar:
        if not nome.strip() or not email.strip():
            st.error("Preencha todos os campos obrigatórios " "(Nome e E-mail).")

        else:
            try:
                editarPessoa(
                    idPessoa=financeiro.pessoa_id,
                    nome=nome.strip(),
                    email=email.strip(),
                    telefone=(telefone.strip() if telefone.strip() else None),
                )

                st.session_state.form_key_edit_financeiro += 1
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as erro:
                st.error("Erro ao salvar os dados no banco: " f"{erro}")

            except Exception as erro:
                st.error(str(erro))
