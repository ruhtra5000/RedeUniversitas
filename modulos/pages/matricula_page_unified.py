import streamlit as st
from modulos.listagem.listagem_matricula_page import telaListagemMatriculas
from modulos.cadastros.pages.matricula_page import telaCadastroMatricula
from modulos.view.view_matricula_page import view_matricula

def tela_matricula_unificada():
    # Verifica se há um ID na sessão solicitando a view
    consulta_id = st.session_state.get("consulta_matricula_id")
    
    if consulta_id:
        view_matricula()
    else:
        aba_listagem, aba_cadastro = st.tabs(["📋 Listagem", "➕ Novo Cadastro"])
        
        with aba_listagem:
            telaListagemMatriculas()
            
        with aba_cadastro:
            telaCadastroMatricula()
