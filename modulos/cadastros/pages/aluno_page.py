import re
import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from database.entidades.Pessoa import Pessoa
from modulos.academico.academico_service import (existeCpf, existeEmail, listarCampus, listarCursos)
from modulos.cadastros.aluno import criarAluno
from modulos.utils.cadastro_visual import (painelCadastro, renderizarAvisoCadastro, renderizarBotaoCadastro, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro)

# Tela de cadastro para Alunos
def telaCadastroAluno():
    if "form_key_aluno" not in st.session_state:
        st.session_state.form_key_aluno = 0

    # Função para voltar à página de cadastros
    def voltarCadastros():
        from modulos.rotas import cadastros_page

        st.switch_page(cadastros_page)

    renderizarTopoCadastro(
        titulo="Cadastrar aluno",
        descricao=("Inclua um novo estudante e defina seu vínculo " "acadêmico."),
        aoVoltar=voltarCadastros,
        prefixoChave="cadastro_aluno",
    )

    if st.session_state.pop("cadastro_realizado", False):
        st.toast(
            "Aluno cadastrado com sucesso!",
            icon=":material/check:",
        )

    if "cache_campus" not in st.session_state:
        st.session_state.cache_campus = listarCampus()

    if "cache_cursos" not in st.session_state:
        st.session_state.cache_cursos = listarCursos()

    lista_campus = st.session_state.cache_campus
    lista_cursos = st.session_state.cache_cursos

    if not lista_campus or not lista_cursos:
        renderizarAvisoCadastro(
            titulo="Campus e curso necessários",
            descricao=(
                "Cadastre pelo menos um campus e um curso "
                "antes de adicionar um aluno."
            ),
        )

    with painelCadastro(
        titulo="Informações do aluno",
        descricao=("Preencha os dados pessoais e selecione o " "vínculo acadêmico."),
    ):

        renderizarSecaoCadastro(
            numero=1,
            titulo="Dados pessoais",
            descricao="Informações de identificação e contato.",
        )

        colNome, colEmail = st.columns(2)

        with colNome:
            nome = st.text_input(
                "Nome completo *",
                placeholder="Ex.: João da Silva",
                key=(f"aluno_nome_" f"{st.session_state.form_key_aluno}"),
            )

        with colEmail:
            email = st.text_input(
                "E-mail *",
                placeholder="email@exemplo.com",
                key=(f"aluno_email_" f"{st.session_state.form_key_aluno}"),
            )

        colCpf, colTelefone = st.columns(2)

        with colCpf:
            cpf = st.text_input(
                "CPF *",
                placeholder="Somente números",
                key=(f"aluno_cpf_" f"{st.session_state.form_key_aluno}"),
            )

        with colTelefone:
            telefone = st.text_input(
                "Telefone",
                placeholder="Opcional",
                key=(f"aluno_telefone_" f"{st.session_state.form_key_aluno}"),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Dados acadêmicos",
            descricao="Campus e curso em que o aluno será matriculado.",
        )

        colCampus, colCurso = st.columns(2)

        with colCampus:
            campus = st.selectbox(
                "Campus *",
                options=lista_campus if lista_campus else [],
                format_func=lambda item: item.nome,
                index=None,
                placeholder="Selecione um campus...",
                disabled=not lista_campus,
                key=(f"aluno_campus_" f"{st.session_state.form_key_aluno}"),
            )

        if campus:
            cursos_filtrados = [
                curso_item
                for curso_item in lista_cursos
                if curso_item.campus_id == campus.id
            ]
        else:
            cursos_filtrados = []

        with colCurso:
            curso = st.selectbox(
                "Curso *",
                options=cursos_filtrados,
                format_func=lambda item: item.nome,
                index=None,
                placeholder=(
                    "Selecione um curso..." if campus else "Selecione o Campus primeiro"
                ),
                disabled=not campus,
                key=(f"aluno_curso_" f"{st.session_state.form_key_aluno}"),
            )

        cadastrar = renderizarBotaoCadastro(
            rotulo="Cadastrar aluno",
            icone=":material/person_add:",
            chave=(f"btn_cad_aluno_" f"{st.session_state.form_key_aluno}"),
        )

    if cadastrar:
        if not lista_campus or not lista_cursos:
            st.error("Cadastre pelo menos um Campus e um Curso " "antes de continuar.")

        elif not nome.strip() or not cpf.strip() or not email.strip():
            st.error("Preencha todos os campos obrigatórios " "(Nome, CPF e E-mail).")

        elif existeCpf(cpf):
            st.error("Já existe um aluno cadastrado com este CPF.")

        elif existeEmail(email.strip()):
            st.error("Já existe um aluno cadastrado com este e-mail.")

        elif campus is None:
            st.error("Por favor, selecione um Campus.")

        elif curso is None:
            st.error("Por favor, selecione um Curso.")

        else:
            try:
                nova_pessoa = Pessoa(
                    nome=nome.strip(),
                    cpf=re.sub(r"\D", "", cpf),
                    email=email.strip(),
                    telefone=(telefone.strip() if telefone.strip() else None),
                )

                criarAluno(
                    pessoa=nova_pessoa,
                    idCampus=campus.id,
                    idCurso=curso.id,
                )

                st.session_state.form_key_aluno += 1
                st.session_state["cadastro_realizado"] = True
                st.session_state.pop("cache_alunos", None)
                st.rerun()

            except SQLAlchemyError as erro:
                st.error("Erro ao salvar os dados no banco: " f"{erro}")

            except Exception as erro:
                st.error("Algo deu errado na criação de aluno: " f"{erro}")
