import streamlit as st
from modulos.academico.academico_service import listarMatriculasGeral
from modulos.utils.listagem_utils import formatar_aprovacao
from modulos.utils.listagem_visual import ColunaListagem, renderizarListagem

# Tela de listagem para Matrículas
def telaListagemMatriculas():

    listaMatriculas = listarMatriculasGeral()

    colunas = [
        ColunaListagem(
            titulo="Aluno",
            valor=lambda matricula: (matricula.aluno.pessoa.nome),
            subtitulo="Matrícula acadêmica",
            proporcao=2.6,
            tipo="principal",
        ),
        ColunaListagem(
            titulo="Disciplina",
            valor=lambda matricula: (matricula.disciplina.nome),
            proporcao=2.5,
        ),
        ColunaListagem(
            titulo="Turma",
            valor=lambda matricula: (
                matricula.turma.codigo or f"Turma {matricula.turma_id}"
            ),
            proporcao=1.8,
        ),
        ColunaListagem(
            titulo="Situação",
            valor=lambda matricula: (formatar_aprovacao(matricula.aprovacao)),
            proporcao=1.7,
            tipo="badge",
        ),
    ]

    # Função de navegação
    def voltar():
        from modulos.rotas import home_page

        st.switch_page(home_page)

    # Função para visualizar detalhes da matricula
    def visualizar(matricula):
        st.session_state["matricula_selecionada"] = {
            "aluno_id": matricula.aluno_id,
            "turma_id": matricula.turma_id,
        }

        from modulos.rotas import (
            view_matricula_page,
        )

        st.switch_page(view_matricula_page)

    renderizarListagem(
        itens=listaMatriculas,
        categoria="Listagem",
        titulo="Matrículas",
        descricao=(
            "Consulte os vínculos acadêmicos dos " "alunos com disciplinas e turmas."
        ),
        singular="matrícula",
        plural="matrículas",
        colunas=colunas,
        obter_id=lambda matricula: (f"{matricula.aluno_id}_" f"{matricula.turma_id}"),
        ao_visualizar=visualizar,
        ao_voltar=voltar,
        prefixo_chave="matricula",
        titulo_tabela="Matrículas cadastradas",
        mensagem_vazia=("Nenhuma matrícula foi cadastrada no sistema."),
    )
