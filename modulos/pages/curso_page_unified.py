import streamlit as st
from modulos.listagem.listagem_curso_page import telaListagemCursos
from modulos.cadastros.pages.curso_page import telaCadastroCurso

def tela_curso_unificada():
    aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
    
    with aba_listagem:
        telaListagemCursos()
        
    with aba_cadastro:
        telaCadastroCurso()
