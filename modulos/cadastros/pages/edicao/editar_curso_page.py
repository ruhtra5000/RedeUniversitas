import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from database.entidades.Curso import ModalidadeCurso
from modulos.academico.academico_service import editarCurso, listarCursoId
from modulos.utils.cadastro_visual import (marcarAcoesCadastro, marcarPainelCadastro, renderizarCabecalhoFormulario, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro)

# Tela de edição para Cursos
def telaEdicaoCurso():
    if "ADMIN" not in st.session_state.roles:
        st.error("Acesso negado. Apenas administradores podem " "editar registros.")
        st.stop()

    curso_id = st.session_state.get("edicao_curso_id")

    if not curso_id:
        st.error("Curso não especificado para edição.")

        if st.button("Voltar"):
            from modulos.rotas import view_curso_page

            st.switch_page(view_curso_page)

        st.stop()

    curso = listarCursoId(curso_id)

    if not curso:
        st.error("Curso não encontrado.")
        st.stop()

    if "form_key_edit_curso" not in st.session_state:
        st.session_state.form_key_edit_curso = 0

    # Função para voltar à página de visualização
    def voltarView():
        st.session_state["consulta_curso_id"] = curso_id
        from modulos.rotas import view_curso_page

        st.switch_page(view_curso_page)

    renderizarTopoCadastro(
        titulo="Editar curso",
        descricao="Atualize a estrutura acadêmica e financeira do curso.",
        aoVoltar=voltarView,
        prefixoChave="edicao_curso",
        categoria="EDIÇÃO",
    )

    if st.session_state.pop("edicao_realizada", False):
        st.toast(
            "Dados do curso atualizados com sucesso!",
            icon=":material/check:",
        )

    modalidades = [modalidade.value for modalidade in ModalidadeCurso]
    modalidade_index = (
        modalidades.index(curso.modalidade.value) if curso.modalidade else 0
    )

    with st.container(border=True):
        marcarPainelCadastro()

        renderizarCabecalhoFormulario(
            titulo=f"Editando {curso.nome}",
            descricao=(
                "Revise os dados acadêmicos, a duração e os valores " "do curso."
            ),
            contexto="EDITANDO REGISTRO",
        )

        renderizarSecaoCadastro(
            numero=1,
            titulo="Informações básicas",
            descricao="Identificação e modalidade de oferta.",
        )

        colNome, colModalidade = st.columns([1.4, 1])

        with colNome:
            nome = st.text_input(
                "Nome do curso *",
                value=curso.nome,
                key=(f"edit_curso_nome_" f"{st.session_state.form_key_edit_curso}"),
            )

        with colModalidade:
            modalidade = st.selectbox(
                "Modalidade *",
                options=modalidades,
                index=modalidade_index,
                key=(
                    f"edit_curso_modalidade_" f"{st.session_state.form_key_edit_curso}"
                ),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Configurações acadêmicas",
            descricao="Carga horária, duração e mensalidade do curso.",
        )

        colMensalidade, colCarga = st.columns(2)

        with colMensalidade:
            mensalidade_base = st.number_input(
                "Mensalidade base (R$) *",
                min_value=0.0,
                value=float(curso.mensalidade_base),
                step=100.0,
                key=(
                    f"edit_curso_mensalidade_" f"{st.session_state.form_key_edit_curso}"
                ),
            )

        with colCarga:
            carga_horaria = st.number_input(
                "Carga horária total (h) *",
                min_value=1,
                value=curso.carga_horaria,
                key=(
                    f"edit_curso_carga_horaria_"
                    f"{st.session_state.form_key_edit_curso}"
                ),
            )

        colDuracaoMin, colDuracaoMax = st.columns(2)

        with colDuracaoMin:
            duracao_min = st.number_input(
                "Duração mínima (semestres) *",
                min_value=1,
                value=curso.dur_min_semestre,
                key=(
                    f"edit_curso_duracao_min_" f"{st.session_state.form_key_edit_curso}"
                ),
            )

        with colDuracaoMax:
            duracao_max = st.number_input(
                "Duração máxima (semestres) *",
                min_value=1,
                value=curso.dur_max_semestre,
                key=(
                    f"edit_curso_duracao_max_" f"{st.session_state.form_key_edit_curso}"
                ),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=3,
            titulo="Vínculo institucional",
            descricao="Unidade responsável pela oferta do curso.",
        )

        st.text_input(
            "Campus",
            value=curso.campus.nome if curso.campus else "",
            disabled=True,
            help="O campus do curso não pode ser alterado diretamente.",
            key=(f"edit_curso_campus_" f"{st.session_state.form_key_edit_curso}"),
        )

        _, centro, _ = st.columns([2, 3, 2])

        with centro:
            marcarAcoesCadastro()

            salvar = st.button(
                "Salvar alterações",
                icon=":material/save:",
                width="stretch",
                type="primary",
                key=(f"btn_edit_curso_" f"{st.session_state.form_key_edit_curso}"),
            )

    if salvar:
        if not nome.strip():
            st.error("Preencha o nome do curso.")

        elif duracao_min > duracao_max:
            st.error("A duração mínima não pode ser maior que a máxima.")

        else:
            try:
                editarCurso(
                    idCurso=curso.id,
                    nome=nome.strip(),
                    modalidade=ModalidadeCurso(modalidade),
                    mensalidade_base=mensalidade_base,
                    carga_horaria=carga_horaria,
                    dur_min_semestre=duracao_min,
                    dur_max_semestre=duracao_max,
                )

                st.session_state.form_key_edit_curso += 1
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as erro:
                st.error("Erro ao salvar os dados no banco: " f"{erro}")

            except Exception as erro:
                st.error(str(erro))
