import streamlit as st
from modulos.academico.academico_service import listarMatriculaId, listarMatricula
from modulos.utils.view_utils import exibirCampo, formatar_aprovacao, limpar_consulta_matricula

# Tela de visualização de matrícula
def telaViewMatricula():

    st.title("🔎 Consulta de Matrícula")
    st.caption(
        "Pesquise utilizando os IDs do aluno e da turma."
    )

    selecionada = st.session_state.pop(
        "matricula_selecionada",    
        None,
    )

    if selecionada:
        st.session_state["consulta_matricula_chave"] = selecionada

    matricula = None

    colVoltar, _ = st.columns([1, 5])

    with colVoltar:
        if st.button("⬅ Voltar", use_container_width=True):
            pass

    with st.form("buscar_matricula", border=True):

        st.markdown("#### 🔍 Buscar matrícula")

        col1, col2 = st.columns(2)

        with col1:
            alunoDigitado = st.text_input(
                "ID do aluno",
                placeholder="Ex.: 1",
                key="consulta_matricula_aluno",
            )

        with col2:
            turmaDigitada = st.text_input(
                "ID da turma",
                placeholder="Ex.: 1",
                key="consulta_matricula_turma",
            )

        colunaBotao, _ = st.columns([1.3, 4.7])

        with colunaBotao:
            buscar = st.form_submit_button(
                "🔍 Buscar",
                type="primary",
                use_container_width=True,
            )

    if buscar:
        st.session_state.pop("consulta_matricula_chave", None)

        idAluno = alunoDigitado.strip()
        idTurma = turmaDigitada.strip()

        if not idAluno or not idTurma:
            st.warning(
                "Informe os IDs do aluno e da turma."
            )

        elif not all(
            valor.isdigit()
            for valor in [idAluno, idTurma]
        ):
            st.error("Todos os IDs devem conter somente números.")

        else:
            matricula = listarMatriculaId(
                int(idAluno),
                int(idTurma),
            )

            if matricula is None:
                st.error("Matrícula não encontrada.")
            else:
                st.session_state["consulta_matricula_chave"] = {
                    "aluno_id": matricula.aluno_id,
                    "turma_id": matricula.turma_id,
                }

    chave = st.session_state.get("consulta_matricula_chave")

    if matricula is None and chave:
        matricula = listarMatriculaId(
            chave["aluno_id"],
            chave["turma_id"],
        )

    if matricula is None:
        if not buscar:
            st.info("Informe os dados para consultar uma matrícula.")

        return

    st.write("")

    titulo, botao = st.columns(
        [4.7, 1.3],
        vertical_alignment="center",
    )

    with titulo:
        st.subheader(
            f"📝 Matrícula de {matricula.aluno.pessoa.nome}"
        )

    with botao:
        st.button(
            "Limpar",
            icon=":material/close:",
            use_container_width=True,
            on_click=limpar_consulta_matricula,
        )

    with st.container(border=True):

        st.markdown("#### 👤 Dados do Aluno")

        col1, col2, col3 = st.columns([1, 3, 2])

        with col1:
            exibirCampo("ID", matricula.aluno_id)

        with col2:
            exibirCampo(
                "Aluno",
                matricula.aluno.pessoa.nome,
            )

        with col3:
            exibirCampo(
                "Matrícula institucional",
                matricula.aluno.matricula,
            )

    st.write("")

    with st.container(border=True):

        st.markdown("#### 📚 Vínculo Acadêmico")

        col1, col2, col3 = st.columns(3)

        with col1:
            exibirCampo(
                "Turma",
                matricula.turma.codigo or
                f"Turma {matricula.turma_id}",
            )

        with col2:
            exibirCampo(
                "Disciplina",
                matricula.disciplina.nome,
            )

        with col3:
            exibirCampo(
                "Situação",
                formatar_aprovacao(matricula.aprovacao),
            )

        st.write("")

        col1, col2, col3 = st.columns(3)

        with col1:
            exibirCampo("ID do aluno", matricula.aluno_id)

        with col2:
            exibirCampo("ID da turma", matricula.turma_id)