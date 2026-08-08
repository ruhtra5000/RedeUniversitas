import streamlit as st
from modulos.listagem.listagem_financeiro_page import telaListagemFinanceiros
from modulos.cadastros.pages.financeiro_page import telaCadastroFinanceiro

def tela_financeiro_unificada():
    aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
    
    with aba_listagem:
        telaListagemFinanceiros()
        
    with aba_cadastro:
        telaCadastroFinanceiro()
