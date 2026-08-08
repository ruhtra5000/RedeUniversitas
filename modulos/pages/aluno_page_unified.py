import streamlit as st
from modulos.listagem.listagem_aluno_page import telaListagemAlunos
from modulos.cadastros.pages.aluno_page import telaCadastroAluno

def tela_aluno_unificada():
    aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
    
    with aba_listagem:
        telaListagemAlunos()
        
    with aba_cadastro:
        telaCadastroAluno()
