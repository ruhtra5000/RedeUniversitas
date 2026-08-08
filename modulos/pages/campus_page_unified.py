import streamlit as st
from modulos.listagem.listagem_campus_page import telaListagemCampus
from modulos.cadastros.pages.campus_page import telaCadastroCampus

def tela_campus_unificada():
    aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
    
    with aba_listagem:
        telaListagemCampus()
        
    with aba_cadastro:
        telaCadastroCampus()
