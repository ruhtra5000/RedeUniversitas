import streamlit as st
from modulos.academico.academico_service import listarDisciplinasGeral
from modulos.utils.listagem_visual import ColunaListagem, renderizarListagem

# Tela de listagem para Disciplinas
def telaListagemDisciplinas():

    listaDisciplinas = listarDisciplinasGeral()

    colunas = [
        ColunaListagem(
            titulo="Disciplina",
            valor=lambda disciplina: disciplina.nome,
            subtitulo="Componente curricular",
            proporcao=2.5,
            tipo="principal",
        ),
        ColunaListagem(
            titulo="Código",
            valor=lambda disciplina: (disciplina.codigo or "Não informado"),
            proporcao=1.4,
        ),
        ColunaListagem(
            titulo="Curso",
            valor=lambda disciplina: (
                disciplina.curso.nome if disciplina.curso else "Não informado"
            ),
            proporcao=2.5,
        ),
        ColunaListagem(
            titulo="Carga",
            valor=lambda disciplina: (f"{disciplina.carga_horaria} h"),
            proporcao=1.1,
        ),
        ColunaListagem(
            titulo="Tipo",
            valor=lambda disciplina: (
                "Obrigatória" if disciplina.obrigatoria else "Optativa"
            ),
            proporcao=1.4,
            tipo="badge",
        ),
    ]

    # Função de navegação
    def voltar():
        from modulos.rotas import home_page

        st.switch_page(home_page)

    # Função para visualizar detalhes da disciplina
    def visualizar(disciplina):
        st.session_state["disciplina_id"] = disciplina.id

        from modulos.rotas import view_disciplina_page

        st.switch_page(view_disciplina_page)

    renderizarListagem(
        itens=listaDisciplinas,
        categoria="Listagem",
        titulo="Disciplinas",
        descricao=(
            "Consulte os componentes curriculares, "
            "códigos, cursos e cargas horárias."
        ),
        singular="disciplina",
        plural="disciplinas",
        colunas=colunas,
        obter_id=lambda disciplina: disciplina.id,
        ao_visualizar=visualizar,
        ao_voltar=voltar,
        prefixo_chave="disciplina",
        titulo_tabela="Disciplinas cadastradas",
        mensagem_vazia=("Nenhuma disciplina foi cadastrada no sistema."),
    )
