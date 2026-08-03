import re
import streamlit as st
from modulos.academico.academico_db import (dbListarProfessorCpf, dbListarProfessorId)
from modulos.utils.view_utils import (formatar_cpf, exibirCampo)

# Função para limpar a consulta de professor
def limpar_consulta_professor():
    st.session_state.pop("consulta_professor_id", None)
    st.session_state.pop("consulta_professor_cpf", None)
    st.session_state.pop("consulta_professor_id_digitado", None)

# Tela de visualização de professor
def telaViewProfessor():

    st.title("🔎 Consulta de Professor")
    st.caption("Pesquise um professor pelo CPF ou pelo ID.")

    if "professor_id" in st.session_state:
        st.session_state["consulta_professor_id"] = (
            st.session_state.pop("professor_id")
        )

    professor = None

    col_voltar, _ = st.columns([1, 5])

    with col_voltar:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import listagem_professor_page
            st.switch_page(listagem_professor_page)

    with st.form("buscar_professor", border=True):

        st.markdown("#### 🔍 Buscar professor")

        col1, col2 = st.columns(2)

        with col1:
            cpf_digitado = st.text_input(
                "CPF",
                placeholder="Somente números",
                key="consulta_professor_cpf",
            )

        with col2:
            id_digitado = st.text_input(
                "ID",
                placeholder="Ex.: 1",
                key="consulta_professor_id_digitado",
            )

        coluna_botao, _ = st.columns([1.3, 4.7])

        with coluna_botao:
            buscar = st.form_submit_button(
                "🔍 Buscar",
                type="primary",
                use_container_width=True,
            )

    if buscar:

        st.session_state.pop("consulta_professor_id", None)

        cpf = re.sub(r"\D", "", cpf_digitado)
        id_professor = id_digitado.strip()

        if not cpf and not id_professor:
            st.warning("Informe um CPF ou um ID.")

        elif cpf and id_professor:
            st.warning("Informe somente o CPF ou somente o ID.")

        elif cpf:
            if len(cpf) != 11:
                st.error("O CPF deve possuir 11 números.")
            else:
                professor = dbListarProfessorCpf(cpf)

                if professor is None:
                    st.error("Professor não encontrado.")
                else:
                    st.session_state["consulta_professor_id"] = (
                        professor.pessoa_id
                    )

        else:
            if not id_professor.isdigit():
                st.error("O ID deve conter somente números.")
            else:
                professor = dbListarProfessorId(int(id_professor))

                if professor is None:
                    st.error("Professor não encontrado.")
                else:
                    st.session_state["consulta_professor_id"] = (
                        professor.pessoa_id
                    )

    professor_id = st.session_state.get("consulta_professor_id")

    if professor is None and professor_id is not None:
        professor = dbListarProfessorId(professor_id)

    if professor is None:
        if not buscar:
            st.info("Informe um CPF ou ID para consultar um professor.")
        return

    st.write("")

    titulo, botao = st.columns(
        [4.7, 1.3],
        vertical_alignment="center",
    )

    with titulo:
        st.subheader(f"👨‍🏫 {professor.pessoa.nome}")

    with botao:
        st.button(
            "Limpar",
            icon=":material/close:",
            use_container_width=True,
            on_click=limpar_consulta_professor,
        )

    with st.container(border=True):

        st.markdown("#### 👤 Dados Pessoais")

        col1, col2 = st.columns([3.5, 2.5])

        with col1:
            exibirCampo(
                "Nome",
                professor.pessoa.nome,
            )

        with col2:
            exibirCampo(
                "CPF",
                formatar_cpf(professor.pessoa.cpf),
            )

        st.write("")

        col1, col2 = st.columns([3.5, 2.5])

        with col1:
            exibirCampo(
                "E-mail",
                professor.pessoa.email,
            )

        with col2:
            exibirCampo(
                "Telefone",
                professor.pessoa.telefone or "Não informado",
            )

    st.write("")

    with st.container(border=True):

        st.markdown("#### 🔗 Vínculo Institucional")

        col1, col2 = st.columns([1.2, 4.8])

        with col1:
            exibirCampo(
                "ID",
                professor.pessoa_id,
            )

        with col2:
            exibirCampo(
                "Campus",
                professor.campus.nome,
            )