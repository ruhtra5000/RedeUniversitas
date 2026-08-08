import streamlit as st
from modulos.listagem.listagem_fornecedor_page import telaListagemFornecedores
from modulos.cadastros.pages.fornecedor_page import telaCadastroFornecedor

def tela_fornecedor_unificada():
    aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
    
    with aba_listagem:
        telaListagemFornecedores()
        
    with aba_cadastro:
        telaCadastroFornecedor()
