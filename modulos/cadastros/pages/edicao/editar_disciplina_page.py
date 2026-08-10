import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from modulos.academico.academico_service import (editarDisciplina, listarDisciplinaId)
from modulos.utils.cadastro_visual import (marcarAcoesCadastro, marcarPainelCadastro, renderizarCabecalhoFormulario, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro)

# Tela de edição para Disciplinas
def telaEdicaoDisciplina():
    if "ADMIN" not in st.session_state.roles:
        st.error("Acesso negado. Apenas administradores podem " "editar registros.")
        st.stop()

    disciplina_id = st.session_state.get("edicao_disciplina_id")

    if not disciplina_id:
        st.error("Disciplina não especificada para edição.")

        if st.button("Voltar"):
            from modulos.rotas import view_disciplina_page

            st.switch_page(view_disciplina_page)

        st.stop()

    disciplina = listarDisciplinaId(disciplina_id)

    if not disciplina:
        st.error("Disciplina não encontrada.")
        st.stop()

    if "form_key_edit_disciplina" not in st.session_state:
        st.session_state.form_key_edit_disciplina = 0

    # Função para voltar à página de visualização
    def voltarView():
        st.session_state["consulta_disciplina_id"] = disciplina_id
        from modulos.rotas import view_disciplina_page

        st.switch_page(view_disciplina_page)

    renderizarTopoCadastro(
        titulo="Editar disciplina",
        descricao="Atualize a identificação e a classificação da disciplina.",
        aoVoltar=voltarView,
        prefixoChave="edicao_disciplina",
        categoria="EDIÇÃO",
    )

    if st.session_state.pop("edicao_realizada", False):
        st.toast(
            "Dados da disciplina atualizados com sucesso!",
            icon=":material/check:",
        )

    with st.container(border=True):
        marcarPainelCadastro()

        renderizarCabecalhoFormulario(
            titulo=f"Editando {disciplina.nome}",
            descricao=(
                "Altere os dados permitidos sem modificar o vínculo "
                "acadêmico existente."
            ),
            contexto="EDITANDO REGISTRO",
        )

        renderizarSecaoCadastro(
            numero=1,
            titulo="Informações básicas",
            descricao="Nome, carga horária e tipo da disciplina.",
        )

        nome = st.text_input(
            "Nome da disciplina *",
            value=disciplina.nome,
            key=(
                f"edit_disciplina_nome_" f"{st.session_state.form_key_edit_disciplina}"
            ),
        )

        colCarga, colTipo = st.columns(2)

        with colCarga:
            st.number_input(
                "Carga horária total (h)",
                min_value=1,
                value=disciplina.carga_horaria,
                disabled=True,
                help=(
                    "A carga horária não pode ser alterada para evitar "
                    "inconsistências em mensalidades."
                ),
                key=(
                    f"edit_disciplina_carga_horaria_"
                    f"{st.session_state.form_key_edit_disciplina}"
                ),
            )

        with colTipo:
            obrigatoria = st.checkbox(
                "Disciplina obrigatória",
                value=disciplina.obrigatoria,
                key=(
                    f"edit_disciplina_obrigatoria_"
                    f"{st.session_state.form_key_edit_disciplina}"
                ),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Vínculo acadêmico",
            descricao="Curso ao qual a disciplina pertence.",
        )

        st.text_input(
            "Curso",
            value=disciplina.curso.nome if disciplina.curso else "",
            disabled=True,
            help="O curso da disciplina não pode ser alterado diretamente.",
            key=(
                f"edit_disciplina_curso_" f"{st.session_state.form_key_edit_disciplina}"
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
                    f"btn_edit_disciplina_"
                    f"{st.session_state.form_key_edit_disciplina}"
                ),
            )

    if salvar:
        if not nome.strip():
            st.error("Preencha o nome da disciplina.")

        else:
            try:
                editarDisciplina(
                    idDisciplina=disciplina.id,
                    nome=nome.strip(),
                    carga_horaria=disciplina.carga_horaria,
                    obrigatoria=obrigatoria,
                )

                st.session_state.form_key_edit_disciplina += 1
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as erro:
                st.error("Erro ao salvar os dados no banco: " f"{erro}")

            except Exception as erro:
                st.error(str(erro))
