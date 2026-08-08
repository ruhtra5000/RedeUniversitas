import streamlit as st
from modulos.listagem.listagem_produto_page import telaListagemProdutos
from modulos.cadastros.pages.estoque_page import telaCadastroEstoque

def tela_estoque_unificada():
    aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
    
    with aba_listagem:
        telaListagemProdutos()
        
    with aba_cadastro:
        telaCadastroEstoque()
