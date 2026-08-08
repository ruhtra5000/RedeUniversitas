import streamlit as st
from modulos.listagem.listagem_disciplina_page import telaListagemDisciplinas
from modulos.cadastros.pages.disciplina_page import telaCadastroDisciplina
from modulos.view.view_disciplina_page import telaViewDisciplina

def tela_disciplina_unificada():
    # Verifica se há um ID na sessão solicitando a view
    consulta_id = st.session_state.get("consulta_disciplina_id")
    
    if consulta_id:
        telaViewDisciplina()
    else:
        aba_listagem, aba_cadastro = st.tabs(["📋 Listagem", "➕ Novo Cadastro"])
        
        with aba_listagem:
            telaListagemDisciplinas()
            
        with aba_cadastro:
            telaCadastroDisciplina()
