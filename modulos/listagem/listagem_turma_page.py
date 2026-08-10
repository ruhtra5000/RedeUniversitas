import streamlit as st
from modulos.academico.academico_service import listarTurmasGeral
from modulos.utils.listagem_visual import ColunaListagem, renderizarListagem

# Tela de listagem para Turmas
def telaListagemTurmas():

    listaTurmas = listarTurmasGeral()

    colunas = [
        ColunaListagem(
            titulo="Disciplina",
            valor=lambda turma: (
                turma.disciplina.nome if turma.disciplina else "Não informada"
            ),
            subtitulo="Turma acadêmica",
            proporcao=2.7,
            tipo="principal",
        ),
        ColunaListagem(
            titulo="Código",
            valor=lambda turma: (turma.codigo or "Não informado"),
            proporcao=1.7,
        ),
        ColunaListagem(
            titulo="Professor",
            valor=lambda turma: (
                turma.professor.pessoa.nome
                if turma.professor and turma.professor.pessoa
                else "Não informado"
            ),
            proporcao=2.7,
        ),
        ColunaListagem(
            titulo="Semestre",
            valor=lambda turma: (turma.semestre or "Não informado"),
            proporcao=1.5,
            tipo="badge",
        ),
    ]

    # Função de navegação
    def voltar():
        from modulos.rotas import home_page

        st.switch_page(home_page)

    # Função para visualizar detalhes da turma
    def visualizar(turma):
        st.session_state["turma_id"] = turma.id

        from modulos.rotas import view_turma_page

        st.switch_page(view_turma_page)

    renderizarListagem(
        itens=listaTurmas,
        categoria="Listagem",
        titulo="Turmas",
        descricao=(
            "Consulte as turmas, disciplinas, " "professores responsáveis e semestres."
        ),
        singular="turma",
        plural="turmas",
        colunas=colunas,
        obter_id=lambda turma: turma.id,
        ao_visualizar=visualizar,
        ao_voltar=voltar,
        prefixo_chave="turma",
        titulo_tabela="Turmas cadastradas",
        mensagem_vazia=("Nenhuma turma foi cadastrada no sistema."),
    )
