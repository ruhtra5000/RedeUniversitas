import streamlit as st
from modulos.listagem.listagem_professor_page import telaListagemProfessores
from modulos.cadastros.pages.professor_page import telaCadastroProfessor
from modulos.view.view_professor_page import telaViewProfessor

def tela_professor_unificada():
    # Verifica se há um ID na sessão solicitando a view
    consulta_id = st.session_state.get("consulta_professor_id") or st.session_state.get("professor_id")
    
    if consulta_id:
        telaViewProfessor()
    else:
        aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
        
        with aba_listagem:
            telaListagemProfessores()
            
        with aba_cadastro:
            telaCadastroProfessor()
