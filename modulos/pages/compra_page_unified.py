import streamlit as st
from modulos.listagem.listagem_compra_page import telaListagemCompras
from modulos.cadastros.pages.compra_page import telaCadastroCompra
from modulos.view.view_compra_page import view_compra

def tela_compra_unificada():
    # Verifica se há um ID na sessão solicitando a view
    consulta_id = st.session_state.get("consulta_compra_id")
    
    if consulta_id:
        view_compra()
    else:
        aba_listagem, aba_cadastro = st.tabs(["📋 Listagem", "➕ Novo Cadastro"])
        
        with aba_listagem:
            telaListagemCompras()
            
        with aba_cadastro:
            telaCadastroCompra()
