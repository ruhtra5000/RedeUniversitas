import streamlit as st
from modulos.academico.academico_service import listarCursos
from modulos.utils.listagem_utils import formatar_modalidade
from modulos.utils.listagem_visual import ColunaListagem, renderizarListagem

# Tela de listagem para Cursos
def telaListagemCursos():

    listaCursos = listarCursos()

    colunas = [
        ColunaListagem(
            titulo="Curso",
            valor=lambda curso: curso.nome,
            subtitulo="Curso acadêmico",
            proporcao=2.7,
            tipo="principal",
        ),
        ColunaListagem(
            titulo="Modalidade",
            valor=lambda curso: formatar_modalidade(curso.modalidade),
            proporcao=1.8,
            tipo="badge",
        ),
        ColunaListagem(
            titulo="Campus",
            valor=lambda curso: (
                curso.campus.nome if curso.campus else "Não informado"
            ),
            proporcao=2.7,
        ),
        ColunaListagem(
            titulo="Carga horária",
            valor=lambda curso: (f"{curso.carga_horaria} h"),
            proporcao=1.4,
        ),
    ]

    # Função de navegação
    def voltar():
        from modulos.rotas import home_page

        st.switch_page(home_page)

    # Função para visualizar detalhes do curso
    def visualizar(curso):
        st.session_state["curso_id"] = curso.id

        from modulos.rotas import view_curso_page

        st.switch_page(view_curso_page)

    renderizarListagem(
        itens=listaCursos,
        categoria="Listagem",
        titulo="Cursos",
        descricao=(
            "Consulte os cursos oferecidos, suas "
            "modalidades, campus e cargas horárias."
        ),
        singular="curso",
        plural="cursos",
        colunas=colunas,
        obter_id=lambda curso: curso.id,
        ao_visualizar=visualizar,
        ao_voltar=voltar,
        prefixo_chave="curso",
        titulo_tabela="Cursos cadastrados",
        mensagem_vazia=("Nenhum curso foi cadastrado no sistema."),
    )
