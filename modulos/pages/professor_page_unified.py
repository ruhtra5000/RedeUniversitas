import streamlit as st
from modulos.listagem.listagem_professor_page import telaListagemProfessores
from modulos.cadastros.pages.professor_page import telaCadastroProfessor

def tela_professor_unificada():
    aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
    
    with aba_listagem:
        telaListagemProfessores()
        
    with aba_cadastro:
        telaCadastroProfessor()
