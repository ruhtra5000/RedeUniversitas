import streamlit as st
from modulos.listagem.listagem_almoxarife_page import telaListagemAlmoxarifes
from modulos.cadastros.pages.almoxarife_page import telaCadastroAlmoxarife

def tela_almoxarife_unificada():
    aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
    
    with aba_listagem:
        telaListagemAlmoxarifes()
        
    with aba_cadastro:
        telaCadastroAlmoxarife()
