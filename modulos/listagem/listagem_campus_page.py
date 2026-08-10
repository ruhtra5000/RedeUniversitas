import streamlit as st
from modulos.academico.academico_service import listarCampus
from modulos.utils.listagem_utils import formatar_cnpj
from modulos.utils.listagem_visual import ColunaListagem, renderizarListagem

# Tela de listagem para Campus
def telaListagemCampus():

    listaCampus = listarCampus()

    colunas = [
        ColunaListagem(
            titulo="Campus",
            valor=lambda campus: campus.nome,
            subtitulo="Unidade institucional",
            proporcao=2.7,
            tipo="principal",
        ),
        ColunaListagem(
            titulo="CNPJ",
            valor=lambda campus: formatar_cnpj(campus.cnpj),
            proporcao=2,
        ),
        ColunaListagem(
            titulo="E-mail",
            valor=lambda campus: (campus.email or "Não informado"),
            proporcao=2.7,
        ),
        ColunaListagem(
            titulo="Telefone",
            valor=lambda campus: (campus.telefone or "Não informado"),
            proporcao=1.8,
        ),
    ]

    # Função de navegação
    def voltar():
        from modulos.rotas import home_page

        st.switch_page(home_page)

    # Função para visualizar detalhes do campus
    def visualizar(campus):
        st.session_state["campus_id"] = campus.id

        from modulos.rotas import view_campus_page

        st.switch_page(view_campus_page)

    renderizarListagem(
        itens=listaCampus,
        categoria="Listagem",
        titulo="Campus",
        descricao=("Consulte as unidades institucionais " "cadastradas no sistema."),
        singular="campus",
        plural="campus",
        colunas=colunas,
        obter_id=lambda campus: campus.id,
        ao_visualizar=visualizar,
        ao_voltar=voltar,
        prefixo_chave="campus",
        titulo_tabela="Campus cadastrados",
        mensagem_vazia=("Nenhum campus foi cadastrado no sistema."),
    )
