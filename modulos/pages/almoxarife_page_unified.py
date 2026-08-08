import streamlit as st
from modulos.listagem.listagem_almoxarife_page import telaListagemAlmoxarifes
from modulos.cadastros.pages.almoxarife_page import telaCadastroAlmoxarife
from modulos.view.view_almoxarife_page import telaViewAlmoxarife

def tela_almoxarife_unificada():
    # Verifica se há um ID na sessão solicitando a view
    consulta_id = st.session_state.get("consulta_almoxarife_id")
    
    if consulta_id:
        telaViewAlmoxarife()
    else:
        aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
        
        with aba_listagem:
            telaListagemAlmoxarifes()
            
        with aba_cadastro:
            telaCadastroAlmoxarife()
