import streamlit as st
from database.entidades.Disciplina import Disciplina
from modulos.academico.academico_service import (listarCursos, listarDisciplinasGeral)
from modulos.cadastros.disciplina import criarDisciplina
from modulos.utils.cadastro_visual import (painelCadastro, renderizarAvisoCadastro, renderizarBotaoCadastro, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro)

# Tela de cadastro para Disciplinas
def telaCadastroDisciplina():
    if "form_key_disc" not in st.session_state:
        st.session_state.form_key_disc = 0

    # Função para voltar à página de cadastros
    def voltarCadastros():
        from modulos.rotas import cadastros_page

        st.switch_page(cadastros_page)

    renderizarTopoCadastro(
        titulo="Cadastrar disciplina",
        descricao=(
            "Adicione um novo componente curricular e configure " "seus pré-requisitos."
        ),
        aoVoltar=voltarCadastros,
        prefixoChave="cadastro_disciplina",
    )

    if st.session_state.pop("cadastro_disc_realizado", False):
        st.toast(
            "Disciplina cadastrada com sucesso!",
            icon=":material/check:",
        )

    if "cache_cursos" not in st.session_state:
        st.session_state.cache_cursos = listarCursos()

    if "cache_disciplinas" not in st.session_state:
        st.session_state.cache_disciplinas = listarDisciplinasGeral()

    lista_cursos = st.session_state.cache_cursos
    lista_disciplinas_existentes = st.session_state.cache_disciplinas

    if not lista_cursos:
        renderizarAvisoCadastro(
            titulo="Curso necessário",
            descricao=(
                "Cadastre pelo menos um curso antes de adicionar " "uma disciplina."
            ),
        )

    with painelCadastro(
        titulo="Informações da disciplina",
        descricao=("Defina os dados acadêmicos e as dependências " "curriculares."),
    ):

        renderizarSecaoCadastro(
            numero=1,
            titulo="Dados da disciplina",
            descricao="Identificação, curso vinculado e carga horária.",
        )

        nome = st.text_input(
            "Nome da disciplina *",
            placeholder="Ex.: Banco de Dados I",
            key=(f"disc_nome_" f"{st.session_state.form_key_disc}"),
        )

        colCurso, colCarga = st.columns([3, 1])

        with colCurso:
            curso_selecionado = st.selectbox(
                "Curso vinculado *",
                options=lista_cursos if lista_cursos else [],
                format_func=lambda item: item.nome,
                index=None,
                placeholder="Selecione um curso...",
                disabled=not lista_cursos,
                key=(f"disc_curso_" f"{st.session_state.form_key_disc}"),
            )

        with colCarga:
            carga_horaria = st.number_input(
                "Carga horária (horas) *",
                min_value=1,
                value=60,
                step=10,
                key=(f"disc_ch_" f"{st.session_state.form_key_disc}"),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Configuração acadêmica",
            descricao="Obrigatoriedade e disciplinas pré-requisito.",
        )

        obrigatoria_str = st.selectbox(
            "Disciplina obrigatória? *",
            options=["Sim", "Não"],
            key=(f"disc_obrigatoria_" f"{st.session_state.form_key_disc}"),
        )
        obrigatoria = obrigatoria_str == "Sim"

        if curso_selecionado:
            disciplinas_filtradas = [
                disciplina
                for disciplina in lista_disciplinas_existentes
                if disciplina.curso_id == curso_selecionado.id
            ]
        else:
            disciplinas_filtradas = []

        pre_requisitos_selecionados = st.multiselect(
            "Pré-requisitos",
            options=disciplinas_filtradas,
            format_func=lambda item: item.nome,
            placeholder=(
                "Selecione uma ou mais disciplinas..."
                if curso_selecionado
                else "Selecione o Curso primeiro"
            ),
            help=("Opcional. Selecione as disciplinas que são " "pré-requisito."),
            disabled=not curso_selecionado,
            key=(f"disc_prereq_" f"{st.session_state.form_key_disc}"),
        )

        cadastrar = renderizarBotaoCadastro(
            rotulo="Cadastrar disciplina",
            icone=":material/post_add:",
            chave=(f"btn_cad_disc_" f"{st.session_state.form_key_disc}"),
        )

    if cadastrar:
        if not lista_cursos:
            st.error("Cadastre pelo menos um Curso antes de continuar.")

        elif not nome.strip():
            st.error("Por favor, preencha o Nome da Disciplina.")

        elif curso_selecionado is None:
            st.error("Por favor, selecione um Curso.")

        else:
            try:
                curso_id = curso_selecionado.id
                lista_pre_req_ids = [
                    disciplina.id for disciplina in pre_requisitos_selecionados
                ]

                nova_disciplina = Disciplina(
                    nome=nome.strip(),
                    carga_horaria=carga_horaria,
                    obrigatoria=obrigatoria,
                    curso_id=curso_id,
                    codigo="",
                )

                criarDisciplina(
                    disciplina=nova_disciplina,
                    preRequisitos=lista_pre_req_ids,
                )

                st.session_state.form_key_disc += 1
                st.session_state["cadastro_disc_realizado"] = True
                st.session_state.pop("cache_disciplinas", None)
                st.rerun()

            except Exception as erro:
                st.error(str(erro))
