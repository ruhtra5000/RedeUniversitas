import streamlit as st
from modulos.listagem.listagem_compra_page import telaListagemCompras
from modulos.cadastros.pages.compra_page import telaCadastroCompra
from modulos.view.view_compra_page import telaViewCompra

def tela_compra_unificada():
    # Verifica se há um ID na sessão solicitando a view
    consulta_id = st.session_state.get("consulta_compra_id") or st.session_state.get("compra_id")
    
    if consulta_id:
        telaViewCompra()
    else:
        aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
        
        with aba_listagem:
            telaListagemCompras()
            
        with aba_cadastro:
            telaCadastroCompra()
