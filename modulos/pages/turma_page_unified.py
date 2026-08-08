import streamlit as st
from modulos.listagem.listagem_turma_page import telaListagemTurmas
from modulos.cadastros.pages.turma_page import telaCadastroTurma

def tela_turma_unificada():
    aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
    
    with aba_listagem:
        telaListagemTurmas()
        
    with aba_cadastro:
        telaCadastroTurma()
