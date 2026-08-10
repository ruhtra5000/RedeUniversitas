import streamlit as st
from modulos.academico.academico_service import listarProfessores
from modulos.utils.listagem_utils import formatar_cpf
from modulos.utils.listagem_visual import ColunaListagem, renderizarListagem

# Tela de listagem para Professores
def telaListagemProfessores():

    listaProfessores = listarProfessores()

    colunas = [
        ColunaListagem(
            titulo="Professor",
            valor=lambda professor: (professor.pessoa.nome),
            subtitulo="Professor",
            proporcao=2.6,
            tipo="principal",
        ),
        ColunaListagem(
            titulo="CPF",
            valor=lambda professor: formatar_cpf(professor.pessoa.cpf),
            proporcao=1.7,
        ),
        ColunaListagem(
            titulo="E-mail",
            valor=lambda professor: (professor.pessoa.email or "Não informado"),
            proporcao=2.5,
        ),
        ColunaListagem(
            titulo="Campus",
            valor=lambda professor: (
                professor.campus.nome if professor.campus else "Não informado"
            ),
            proporcao=2.7,
            tipo="badge",
        ),
    ]

    # Função de navegação
    def voltar():
        from modulos.rotas import home_page

        st.switch_page(home_page)

    # Função para visualizar detalhes do professor
    def visualizar(professor):
        st.session_state["professor_id"] = professor.pessoa_id

        from modulos.rotas import (
            view_professor_page,
        )

        st.switch_page(view_professor_page)

    renderizarListagem(
        itens=listaProfessores,
        categoria="Listagem",
        titulo="Professores",
        descricao=(
            "Consulte os docentes cadastrados e " "seus vínculos institucionais."
        ),
        singular="professor",
        plural="professores",
        colunas=colunas,
        obter_id=lambda professor: (professor.pessoa_id),
        ao_visualizar=visualizar,
        ao_voltar=voltar,
        prefixo_chave="professor",
        titulo_tabela="Professores cadastrados",
        mensagem_vazia=("Nenhum professor foi cadastrado no sistema."),
    )
