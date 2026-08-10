import streamlit as st
from modulos.estoque.estoque_service import listarAlmoxarifes
from modulos.utils.listagem_utils import formatar_cpf
from modulos.utils.listagem_visual import ColunaListagem, renderizarListagem

# Tela de listagem para Almoxarifes
def telaListagemAlmoxarifes():

    listaAlmoxarifes = listarAlmoxarifes()

    colunas = [
        ColunaListagem(
            titulo="Profissional",
            valor=lambda almoxarife: (almoxarife.pessoa.nome),
            subtitulo="Almoxarife",
            proporcao=2.6,
            tipo="principal",
        ),
        ColunaListagem(
            titulo="CPF",
            valor=lambda almoxarife: formatar_cpf(almoxarife.pessoa.cpf),
            proporcao=1.7,
        ),
        ColunaListagem(
            titulo="E-mail",
            valor=lambda almoxarife: (almoxarife.pessoa.email or "Não informado"),
            proporcao=2.5,
        ),
        ColunaListagem(
            titulo="Campus",
            valor=lambda almoxarife: (
                almoxarife.campus.nome if almoxarife.campus else "Não informado"
            ),
            proporcao=3,
            tipo="badge",
        ),
    ]

    # Função de navegação
    def voltar():
        from modulos.rotas import home_page

        st.switch_page(home_page)

    # Função para visualizar detalhes do almoxarife
    def visualizar(almoxarife):
        st.session_state["almoxarife_id"] = almoxarife.pessoa_id

        from modulos.rotas import view_almoxarife_page

        st.switch_page(view_almoxarife_page)

    renderizarListagem(
        itens=listaAlmoxarifes,
        categoria="Listagem",
        titulo="Almoxarifes",
        descricao=(
            "Profissionais responsáveis pelo controle " "dos almoxarifados dos campus."
        ),
        singular="registro",
        plural="registros",
        colunas=colunas,
        obter_id=lambda almoxarife: (almoxarife.pessoa_id),
        ao_visualizar=visualizar,
        ao_voltar=voltar,
        prefixo_chave="almoxarife",
        mensagem_vazia=("Nenhum almoxarife foi cadastrado " "no sistema."),
    )
