import streamlit as st
from modulos.academico.academico_service import listarAlunos
from modulos.utils.listagem_visual import ColunaListagem, renderizarListagem

# Tela de listagem para Alunos
def telaListagemAlunos():

    listaAlunos = listarAlunos()

    colunas = [
        ColunaListagem(
            titulo="Aluno",
            valor=lambda aluno: (aluno.pessoa.nome or "Nome não informado"),
            subtitulo="Aluno",
            proporcao=2.6,
            tipo="principal",
        ),
        ColunaListagem(
            titulo="Matrícula",
            valor=lambda aluno: (aluno.matricula or "Não informado"),
            proporcao=1.6,
        ),
        ColunaListagem(
            titulo="Curso",
            valor=lambda aluno: (aluno.curso.nome if aluno.curso else "Não informado"),
            proporcao=2.5,
        ),
        ColunaListagem(
            titulo="Campus",
            valor=lambda aluno: (
                aluno.campus.nome if aluno.campus else "Não informado"
            ),
            proporcao=2.7,
            tipo="badge",
        ),
    ]

    # Função de navegação
    def voltar():
        from modulos.rotas import home_page

        st.switch_page(home_page)

    # Função para visualizar detalhes do aluno
    def visualizar(aluno):
        st.session_state["aluno_id"] = aluno.pessoa_id

        from modulos.rotas import view_aluno_page

        st.switch_page(view_aluno_page)

    renderizarListagem(
        itens=listaAlunos,
        categoria="Listagem",
        titulo="Alunos",
        descricao=(
            "Consulte os estudantes cadastrados, " "suas matrículas, cursos e campus."
        ),
        singular="aluno",
        plural="alunos",
        colunas=colunas,
        obter_id=lambda aluno: aluno.pessoa_id,
        ao_visualizar=visualizar,
        ao_voltar=voltar,
        prefixo_chave="aluno",
        titulo_tabela="Alunos cadastrados",
        mensagem_vazia=("Nenhum aluno foi cadastrado no sistema."),
    )
