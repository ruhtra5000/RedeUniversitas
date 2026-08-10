import re
import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from database.entidades.Pessoa import Pessoa
from modulos.academico.academico_service import listarCampus
from modulos.cadastros.professor import criarProfessor
from modulos.utils.cadastro_visual import (painelCadastro, renderizarAvisoCadastro, renderizarBotaoCadastro, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro)

# Tela de cadastro para Professores
def telaCadastroProfessor():
    if "form_key_prof" not in st.session_state:
        st.session_state.form_key_prof = 0

    # Função para voltar à página de cadastros
    def voltarCadastros():
        from modulos.rotas import cadastros_page

        st.switch_page(cadastros_page)

    renderizarTopoCadastro(
        titulo="Cadastrar professor",
        descricao=(
            "Inclua um novo docente e defina o campus em que " "ficará vinculado."
        ),
        aoVoltar=voltarCadastros,
        prefixoChave="cadastro_professor",
    )

    if st.session_state.pop("cadastro_prof_realizado", False):
        st.toast(
            "Professor cadastrado com sucesso!",
            icon=":material/check:",
        )

    if "cache_campus" not in st.session_state:
        st.session_state.cache_campus = listarCampus()

    lista_campus = st.session_state.cache_campus

    if not lista_campus:
        renderizarAvisoCadastro(
            titulo="Campus necessário",
            descricao=(
                "Cadastre pelo menos um campus antes de adicionar " "um professor."
            ),
        )

    with painelCadastro(
        titulo="Informações do professor",
        descricao=(
            "Preencha os dados pessoais e o vínculo " "institucional do docente."
        ),
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
                placeholder="Ex.: Carlos Mendes",
                key=(f"prof_nome_" f"{st.session_state.form_key_prof}"),
            )

        with colEmail:
            email = st.text_input(
                "E-mail *",
                placeholder="email@exemplo.com",
                key=(f"prof_email_" f"{st.session_state.form_key_prof}"),
            )

        colCpf, colTelefone = st.columns(2)

        with colCpf:
            cpf = st.text_input(
                "CPF *",
                placeholder="Somente números",
                key=(f"prof_cpf_" f"{st.session_state.form_key_prof}"),
            )

        with colTelefone:
            telefone = st.text_input(
                "Telefone",
                placeholder="Opcional",
                key=(f"prof_telefone_" f"{st.session_state.form_key_prof}"),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Vínculo institucional",
            descricao="Campus em que o professor atuará.",
        )

        campus = st.selectbox(
            "Campus *",
            options=lista_campus if lista_campus else [],
            format_func=lambda item: item.nome,
            index=None,
            placeholder="Selecione um campus...",
            disabled=not lista_campus,
            key=(f"prof_campus_" f"{st.session_state.form_key_prof}"),
        )

        cadastrar = renderizarBotaoCadastro(
            rotulo="Cadastrar professor",
            icone=":material/person_add:",
            chave=(f"btn_cad_prof_" f"{st.session_state.form_key_prof}"),
        )

    if cadastrar:
        if not lista_campus:
            st.error("Cadastre pelo menos um Campus antes de continuar.")

        elif not nome.strip() or not cpf.strip() or not email.strip():
            st.error("Por favor, preencha todos os campos obrigatórios.")

        elif campus is None:
            st.error("Por favor, selecione um Campus.")

        else:
            try:
                nova_pessoa = Pessoa(
                    nome=nome.strip(),
                    cpf=re.sub(r"\D", "", cpf),
                    email=email.strip(),
                    telefone=(telefone.strip() if telefone.strip() else None),
                )

                criarProfessor(
                    pessoa=nova_pessoa,
                    idCampus=campus.id,
                )

                st.session_state.form_key_prof += 1
                st.session_state["cadastro_prof_realizado"] = True
                st.session_state.pop("cache_professores", None)
                st.rerun()

            except SQLAlchemyError as erro:
                st.error("Erro ao salvar os dados no banco: " f"{erro}")

            except Exception as erro:
                st.error(str(erro))
