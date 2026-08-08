import streamlit as st
from modulos.listagem.listagem_matricula_page import telaListagemMatriculas
from modulos.cadastros.pages.matricula_page import telaCadastroMatricula

def tela_matricula_unificada():
    aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
    
    with aba_listagem:
        telaListagemMatriculas()
        
    with aba_cadastro:
        telaCadastroMatricula()
