import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from database.entidades.Curso import Curso
from database.entidades.enums.ModalidadeCurso import ModalidadeCurso
from modulos.academico.academico_service import (listarCampus, listarProfessores)
from modulos.cadastros.curso import criarCurso
from modulos.utils.cadastro_visual import (painelCadastro, renderizarBotaoCadastro, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro)

# Tela de cadastro para Cursos
def telaCadastroCurso():
    if "form_key_curso" not in st.session_state:
        st.session_state.form_key_curso = 0

    # Função para voltar à página de cadastros
    def voltarCadastros():
        from modulos.rotas import cadastros_page

        st.switch_page(cadastros_page)

    renderizarTopoCadastro(
        titulo="Cadastrar curso",
        descricao=(
            "Crie uma nova formação acadêmica e configure "
            "seus vínculos institucionais."
        ),
        aoVoltar=voltarCadastros,
        prefixoChave="cadastro_curso",
    )

    if st.session_state.pop("cadastro_curso_realizado", False):
        st.toast(
            "Curso cadastrado com sucesso!",
            icon=":material/check:",
        )

    if "cache_campus" not in st.session_state:
        st.session_state.cache_campus = listarCampus()

    if "cache_professores" not in st.session_state:
        st.session_state.cache_professores = listarProfessores()

    lista_campus = st.session_state.cache_campus
    lista_professores = st.session_state.cache_professores

    with painelCadastro(
        titulo="Informações do curso",
        descricao=(
            "Defina os dados acadêmicos, financeiros e a " "unidade responsável."
        ),
    ):

        renderizarSecaoCadastro(
            numero=1,
            titulo="Dados principais",
            descricao="Identificação, modalidade e características do curso.",
        )

        colNome, colModalidade, colMensalidade = st.columns([2, 1.4, 1.4])

        with colNome:
            nome = st.text_input(
                "Nome do curso *",
                placeholder="Ex.: Engenharia de Software",
                key=(f"curso_nome_" f"{st.session_state.form_key_curso}"),
            )

        with colModalidade:
            modalidade = st.selectbox(
                "Modalidade *",
                options=list(ModalidadeCurso),
                format_func=(lambda item: item.name.replace("_", " ").title()),
                key=(f"curso_modalidade_" f"{st.session_state.form_key_curso}"),
            )

        with colMensalidade:
            mensalidade_base = st.number_input(
                "Mensalidade base (R$) *",
                min_value=1.0,
                step=50.0,
                format="%.2f",
                key=(f"curso_mensalidade_" f"{st.session_state.form_key_curso}"),
            )

        colCarga, colDurMin, colDurMax = st.columns(3)

        with colCarga:
            carga_horaria = st.number_input(
                "Carga horária total (horas) *",
                min_value=1,
                step=100,
                key=(f"curso_carga_" f"{st.session_state.form_key_curso}"),
            )

        with colDurMin:
            dur_min = st.number_input(
                "Duração mínima (semestres) *",
                min_value=1,
                step=1,
                key=(f"curso_dur_min_" f"{st.session_state.form_key_curso}"),
            )

        with colDurMax:
            dur_max = st.number_input(
                "Duração máxima (semestres) *",
                min_value=1,
                step=1,
                key=(f"curso_dur_max_" f"{st.session_state.form_key_curso}"),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Vínculos institucionais",
            descricao="Campus responsável e coordenação do curso.",
        )

        colCampus, colCoordenador = st.columns(2)

        with colCampus:
            campus_selecionado = st.selectbox(
                "Campus do curso *",
                options=lista_campus if lista_campus else [],
                format_func=lambda item: item.nome,
                index=None,
                placeholder="Selecione um campus...",
                disabled=not lista_campus,
                key=(f"curso_campus_" f"{st.session_state.form_key_curso}"),
            )

        if campus_selecionado:
            professores_filtrados = [
                professor
                for professor in lista_professores
                if professor.campus_id == campus_selecionado.id
            ]
        else:
            professores_filtrados = []

        with colCoordenador:
            coordenador_selecionado = st.selectbox(
                "Coordenador",
                options=professores_filtrados,
                format_func=lambda item: item.pessoa.nome,
                index=None,
                placeholder=(
                    "Selecione um professor..."
                    if campus_selecionado
                    else "Selecione o Campus primeiro"
                ),
                disabled=not campus_selecionado,
                key=(f"curso_coord_" f"{st.session_state.form_key_curso}"),
            )

        cadastrar = renderizarBotaoCadastro(
            rotulo="Cadastrar curso",
            icone=":material/library_add:",
            chave=(f"btn_cad_curso_" f"{st.session_state.form_key_curso}"),
        )

    if cadastrar:
        if not nome.strip():
            st.error("Por favor, informe o Nome do Curso.")

        elif campus_selecionado is None:
            st.error("Por favor, selecione o Campus vinculado.")

        elif dur_min > dur_max:
            st.error("A duração mínima não pode ser maior que a " "duração máxima.")

        else:
            try:
                id_campus = campus_selecionado.id
                id_coordenador = (
                    coordenador_selecionado.pessoa_id
                    if coordenador_selecionado
                    else None
                )

                novo_curso = Curso(
                    nome=nome.strip(),
                    modalidade=modalidade,
                    mensalidade_base=mensalidade_base,
                    carga_horaria=carga_horaria,
                    dur_min_semestre=dur_min,
                    dur_max_semestre=dur_max,
                    campus_id=id_campus,
                    coordenador_id=id_coordenador,
                )

                criarCurso(curso=novo_curso)

                st.session_state.form_key_curso += 1
                st.session_state["cadastro_curso_realizado"] = True
                st.session_state.pop("cache_cursos", None)
                st.rerun()

            except SQLAlchemyError as erro:
                st.error(f"Erro no banco de dados: {erro}")

            except Exception as erro:
                st.error(str(erro))
