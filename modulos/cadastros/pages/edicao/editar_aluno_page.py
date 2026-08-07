from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
import re
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
from modulos.academico.academico_service import listarAlunoId, editarPessoa

def telaEdicaoAluno():
    if "ADMIN" not in st.session_state.roles:
        st.error("Acesso negado. Apenas administradores podem editar registros.")
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

    col1, _ = st.columns([1, 6])
    with col1:
        if st.button(":material/arrow_back: Voltar", width="stretch"):
            st.session_state["consulta_aluno_id"] = aluno_id
            from modulos.rotas import view_aluno_page
            st.switch_page(view_aluno_page)

    st.title(":material/edit: Editar Aluno")
    st.caption("Altere os dados pessoais do aluno.")

    if st.session_state.pop("edicao_realizada", False):
        st.toast("Dados do aluno atualizados com sucesso!", icon=":material/check:")

    with st.container():
        with st.container():
            st.subheader("Dados Pessoais")
            with st.container(horizontal=True):
                nome = st.text_input(
                    "Nome Completo *",
                    value=aluno.pessoa.nome,
                    key=f"edit_aluno_nome_{st.session_state.form_key_edit_aluno}"
                )
                email = st.text_input(
                    "E-mail *",
                    value=aluno.pessoa.email,
                    key=f"edit_aluno_email_{st.session_state.form_key_edit_aluno}"
                )

            with st.container(horizontal=True):
                cpf = st.text_input(
                    "CPF (Somente Leitura)",
                    value=aluno.pessoa.cpf,
                    disabled=True,
                    key=f"edit_aluno_cpf_{st.session_state.form_key_edit_aluno}"
                )
                telefone = st.text_input(
                    "Telefone",
                    value=aluno.pessoa.telefone if aluno.pessoa.telefone else "",
                    key=f"edit_aluno_telefone_{st.session_state.form_key_edit_aluno}"
                )

            st.subheader("Dados Acadêmicos")
            with st.container(horizontal=True):
                st.text_input(
                    "Campus",
                    value=aluno.campus.nome if aluno.campus else "",
                    disabled=True,
                    help="O campus do aluno não pode ser alterado diretamente.",
                    key=f"edit_aluno_campus_{st.session_state.form_key_edit_aluno}"
                )
                st.text_input(
                    "Curso",
                    value=aluno.curso.nome if aluno.curso else "",
                    disabled=True,
                    help="O curso do aluno não pode ser alterado diretamente.",
                    key=f"edit_aluno_curso_{st.session_state.form_key_edit_aluno}"
                )

        st.write("")
        _, centro, _ = st.columns([2, 3, 2])

        with centro:
            salvar = st.button(
                "Salvar Alterações",
                width="stretch",
                type="primary",
                key=f"btn_edit_aluno_{st.session_state.form_key_edit_aluno}"
            )

    if salvar:
        if not nome.strip() or not email.strip():
            st.error("Preencha todos os campos obrigatórios (Nome e E-mail).")
        else:
            try:
                editarPessoa(
                    idPessoa=aluno.pessoa_id,
                    nome=nome.strip(),
                    email=email.strip(),
                    telefone=telefone.strip() if telefone.strip() else None
                )
                st.session_state.form_key_edit_aluno += 1 
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(f"{str(e)}")
