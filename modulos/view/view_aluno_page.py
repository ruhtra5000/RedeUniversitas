import re
import streamlit as st
from modulos.academico.academico_service import listarAlunoCpf, listarAlunoId
from modulos.utils.view_utils import exibirCampo, limpar_consulta_aluno, formatar_cpf
        
# Tela de visualização de aluno
def telaViewAluno():

    st.title("🔎 Consulta de Aluno")
    st.caption("Pesquise um aluno pelo CPF ou pelo ID.")

    # Recebe o aluno selecionado pela listagem
    if "aluno_id" in st.session_state:
        st.session_state["consulta_aluno_id"] = st.session_state.pop("aluno_id")

    aluno = None

    # Voltar para a listagem
    col_voltar, _ = st.columns([1, 5])

    with col_voltar:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import listagem_aluno_page
            st.switch_page(listagem_aluno_page)

    # Pesquisa
    with st.form("buscar_aluno", border=True):

        st.markdown("#### 🔍 Buscar aluno")

        col1, col2 = st.columns(2)

        with col1:
            cpf_digitado = st.text_input(
                "CPF",
                placeholder="Somente números",
                key="consulta_cpf",
            )

        with col2:
            id_digitado = st.text_input(
                "ID",
                placeholder="Ex.: 1",
                key="consulta_id",
            )

        coluna_botao, _ = st.columns([1.3, 4.7])

        with coluna_botao:
            buscar = st.form_submit_button(
                "🔍 Buscar",
                type="primary",
                use_container_width=True,
            )

    if buscar:

        st.session_state.pop("consulta_aluno_id", None)

        cpf = re.sub(r"\D", "", cpf_digitado)
        id_aluno = id_digitado.strip()

        if not cpf and not id_aluno:
            st.warning("Informe um CPF ou um ID.")

        elif cpf and id_aluno:
            st.warning("Informe somente o CPF ou somente o ID.")

        elif cpf:
            if len(cpf) != 11:
                st.error("O CPF deve possuir 11 números.")
            else:
                aluno = listarAlunoCpf(cpf)

                if aluno is None:
                    st.error("Aluno não encontrado.")
                else:
                    st.session_state["consulta_aluno_id"] = aluno.pessoa_id

        else:
            if not id_aluno.isdigit():
                st.error("O ID deve conter somente números.")
            else:
                aluno = listarAlunoId(int(id_aluno))

                if aluno is None:
                    st.error("Aluno não encontrado.")
                else:
                    st.session_state["consulta_aluno_id"] = aluno.pessoa_id

    aluno_id = st.session_state.get("consulta_aluno_id")

    if aluno is None and aluno_id is not None:
        aluno = listarAlunoId(aluno_id)

    if aluno is None:
        if not buscar:
            st.info("Informe um CPF ou ID para consultar um aluno.")
        return

    st.write("")

    titulo, botao_limpar, botao_editar = st.columns(
        [4.2, 0.9, 0.9],
        vertical_alignment="center",
    )

    with titulo:
        st.subheader(f"🎓 {aluno.pessoa.nome}")

    with botao_limpar:
        st.button(
            "Limpar",
            icon=":material/close:",
            use_container_width=True,
            on_click=limpar_consulta_aluno,
        )

    with botao_editar:
        if "ADMIN" in st.session_state.roles:
            if st.button(
                "Editar",
                icon=":material/edit:",
                use_container_width=True,
                type="secondary"
            ):
                st.session_state["edicao_aluno_id"] = aluno.pessoa_id
                from modulos.rotas import editar_aluno_page
                st.switch_page(editar_aluno_page)

    with st.container(border=True):

        st.markdown("#### 👤 Dados Pessoais")

        col1, col2 = st.columns([3.5, 2.5])

        with col1:
            exibirCampo("Nome", aluno.pessoa.nome)

        with col2:
            exibirCampo("CPF", aluno.pessoa.cpf)
            formatar_cpf(aluno.pessoa.cpf)

        st.write("")

        col1, col2 = st.columns([3.5, 2.5])

        with col1:
            exibirCampo("E-mail", aluno.pessoa.email)

        with col2:
            exibirCampo(
                "Telefone",
                aluno.pessoa.telefone or "Não informado",
            )

    st.write("")

    with st.container(border=True):

        st.markdown("#### 🎓 Dados Acadêmicos")

        col1, col2, col3 = st.columns([1, 2, 3])

        with col1:
            exibirCampo("ID", aluno.pessoa_id)

        with col2:
            exibirCampo("Matrícula", aluno.matricula)

        with col3:
            exibirCampo("Campus", aluno.campus.nome)

        st.write("")

        col1, col2, col3 = st.columns([3, 1.5, 1.5])

        with col1:
            exibirCampo("Curso", aluno.curso.nome)

        with col2:
            exibirCampo(
                "Média Geral",
                f"{aluno.media_geral or 0:.2f}",
            )

        with col3:
            exibirCampo(
                "Coef. Rendimento",
                f"{aluno.coef_rend or 0:.2f}",
            )