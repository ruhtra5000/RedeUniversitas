import streamlit as st
from modulos.listagem.listagem_disciplina_page import telaListagemDisciplinas
from modulos.cadastros.pages.disciplina_page import telaCadastroDisciplina

def tela_disciplina_unificada():
    aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
    
    with aba_listagem:
        telaListagemDisciplinas()
        
    with aba_cadastro:
        telaCadastroDisciplina()
