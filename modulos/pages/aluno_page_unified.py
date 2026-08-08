import streamlit as st
from modulos.listagem.listagem_aluno_page import telaListagemAlunos
from modulos.cadastros.pages.aluno_page import telaCadastroAluno
from modulos.view.view_aluno_page import telaViewAluno

def tela_aluno_unificada():
    # Verifica se há um ID na sessão solicitando a view
    consulta_id = st.session_state.get("consulta_aluno_id")
    
    if consulta_id:
        telaViewAluno()
    else:
        aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
        
        with aba_listagem:
            telaListagemAlunos()
            
        with aba_cadastro:
            telaCadastroAluno()
