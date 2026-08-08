import streamlit as st
from modulos.listagem.listagem_turma_page import telaListagemTurmas
from modulos.cadastros.pages.turma_page import telaCadastroTurma
from modulos.view.view_turma_page import telaViewTurma

def tela_turma_unificada():
    # Verifica se há um ID na sessão solicitando a view
    consulta_id = st.session_state.get("consulta_turma_id") or st.session_state.get("turma_id")
    
    if consulta_id:
        telaViewTurma()
    else:
        aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
        
        with aba_listagem:
            telaListagemTurmas()
            
        with aba_cadastro:
            telaCadastroTurma()
