import streamlit as st
from modulos.listagem.listagem_compra_page import telaListagemCompras
from modulos.cadastros.pages.compra_page import telaCadastroCompra

def tela_compra_unificada():
    aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
    
    with aba_listagem:
        telaListagemCompras()
        
    with aba_cadastro:
        telaCadastroCompra()
