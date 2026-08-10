import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from database.entidades.Turma import Turma
from modulos.academico.academico_service import (listarCursos, listarDisciplinasGeral, listarProfessores)
from modulos.cadastros.turma import criarTurma
from modulos.utils.cadastro_visual import (painelCadastro, renderizarAvisoCadastro, renderizarBotaoCadastro, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro)

# Tela de cadastro para Turmas
def telaCadastroTurma():
    if "form_key_turma" not in st.session_state:
        st.session_state.form_key_turma = 0

    # Função para voltar à página de cadastros
    def voltarCadastros():
        from modulos.rotas import cadastros_page

        st.switch_page(cadastros_page)

    renderizarTopoCadastro(
        titulo="Cadastrar turma",
        descricao=(
            "Crie uma nova oferta acadêmica e associe disciplina, "
            "professor e semestre."
        ),
        aoVoltar=voltarCadastros,
        prefixoChave="cadastro_turma",
    )

    if st.session_state.pop("cadastro_turma_realizado", False):
        st.toast(
            "Turma cadastrada com sucesso!",
            icon=":material/check:",
        )

    if "cache_cursos" not in st.session_state:
        st.session_state.cache_cursos = listarCursos()

    if "cache_professores" not in st.session_state:
        st.session_state.cache_professores = listarProfessores()

    if "cache_disciplinas" not in st.session_state:
        st.session_state.cache_disciplinas = listarDisciplinasGeral()

    lista_cursos = st.session_state.cache_cursos
    lista_disciplinas = st.session_state.cache_disciplinas
    lista_professores = st.session_state.cache_professores

    if not lista_cursos or not lista_disciplinas or not lista_professores:
        renderizarAvisoCadastro(
            titulo="Cadastros necessários",
            descricao=(
                "É necessário possuir ao menos um curso, uma "
                "disciplina e um professor."
            ),
        )

    with painelCadastro(
        titulo="Informações da turma",
        descricao=(
            "Selecione o curso para visualizar disciplinas e "
            "professores compatíveis."
        ),
    ):

        renderizarSecaoCadastro(
            numero=1,
            titulo="Oferta acadêmica",
            descricao="Curso e disciplina que compõem a turma.",
        )

        colCurso, colDisciplina = st.columns(2)

        with colCurso:
            curso_selecionado = st.selectbox(
                "Curso *",
                options=lista_cursos if lista_cursos else [],
                format_func=lambda item: item.nome,
                index=None,
                placeholder="Selecione um curso...",
                disabled=not lista_cursos,
                key=(f"turma_curso_" f"{st.session_state.form_key_turma}"),
            )

        if curso_selecionado:
            disciplinas_filtradas = [
                disciplina
                for disciplina in lista_disciplinas
                if disciplina.curso_id == curso_selecionado.id
            ]

            professores_filtrados = [
                professor
                for professor in lista_professores
                if professor.campus_id == curso_selecionado.campus_id
            ]
        else:
            disciplinas_filtradas = []
            professores_filtrados = []

        with colDisciplina:
            disciplina_selecionada = st.selectbox(
                "Disciplina *",
                options=disciplinas_filtradas,
                format_func=lambda item: item.nome,
                index=None,
                placeholder=(
                    "Selecione uma disciplina..."
                    if curso_selecionado
                    else "Selecione o Curso primeiro"
                ),
                disabled=not curso_selecionado,
                key=(f"turma_disc_" f"{st.session_state.form_key_turma}"),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Responsável e período",
            descricao="Professor responsável e semestre da oferta.",
        )

        colProfessor, colSemestre = st.columns([3, 1])

        with colProfessor:
            professor_selecionado = st.selectbox(
                "Professor *",
                options=professores_filtrados,
                format_func=lambda item: item.pessoa.nome,
                index=None,
                placeholder=(
                    "Selecione um professor..."
                    if professores_filtrados
                    else (
                        "Nenhum professor disponível neste campus"
                        if curso_selecionado
                        else "Selecione o Curso primeiro"
                    )
                ),
                disabled=not professores_filtrados,
                key=(f"turma_prof_" f"{st.session_state.form_key_turma}"),
            )

        with colSemestre:
            semestre = st.text_input(
                "Semestre *",
                placeholder="Ex.: 2026.1",
                key=(f"turma_semestre_" f"{st.session_state.form_key_turma}"),
            )

        cadastrar = renderizarBotaoCadastro(
            rotulo="Cadastrar turma",
            icone=":material/group_add:",
            chave=(f"btn_cad_turma_" f"{st.session_state.form_key_turma}"),
        )

    if cadastrar:
        if not lista_cursos or not lista_disciplinas or not lista_professores:
            st.error(
                "Cadastre os requisitos básicos "
                "(Curso, Disciplina e Professor) antes de continuar."
            )

        elif not semestre.strip():
            st.error("Por favor, preencha o Semestre.")

        elif curso_selecionado is None:
            st.error("Por favor, selecione um Curso.")

        elif disciplina_selecionada is None:
            st.error("Por favor, selecione uma Disciplina.")

        elif not professores_filtrados:
            st.error(
                "Não existe nenhum professor cadastrado no mesmo "
                "campus do curso selecionado."
            )

        elif professor_selecionado is None:
            st.error("Por favor, selecione um Professor.")

        else:
            try:
                nova_turma = Turma(
                    semestre=semestre.strip(),
                    codigo="",
                    curso_id=curso_selecionado.id,
                    disciplina_id=disciplina_selecionada.id,
                    professor_id=professor_selecionado.pessoa_id,
                )

                criarTurma(
                    turma=nova_turma,
                    curso=curso_selecionado,
                    disciplina=disciplina_selecionada,
                    professor=professor_selecionado,
                )

                st.session_state.form_key_turma += 1
                st.session_state["cadastro_turma_realizado"] = True
                st.session_state.pop("cache_turmas", None)
                st.rerun()

            except SQLAlchemyError as erro:
                st.error(f"Erro no banco de dados: {erro}")

            except Exception as erro:
                st.error(str(erro))
