import streamlit as st
from modulos.listagem.listagem_campus_page import telaListagemCampus
from modulos.cadastros.pages.campus_page import telaCadastroCampus
from modulos.view.view_campus_page import telaViewCampus

def tela_campus_unificada():
    # Verifica se há um ID na sessão solicitando a view
    consulta_id = st.session_state.get("consulta_campus_id")
    
    if consulta_id:
        telaViewCampus()
    else:
        aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
        
        with aba_listagem:
            telaListagemCampus()
            
        with aba_cadastro:
            telaCadastroCampus()
