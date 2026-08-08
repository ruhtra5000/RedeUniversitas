import streamlit as st
from modulos.listagem.listagem_curso_page import telaListagemCursos
from modulos.cadastros.pages.curso_page import telaCadastroCurso
from modulos.view.view_curso_page import telaViewCurso

def tela_curso_unificada():
    # Verifica se há um ID na sessão solicitando a view
    consulta_id = st.session_state.get("consulta_curso_id")
    
    if consulta_id:
        telaViewCurso()
    else:
        aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
        
        with aba_listagem:
            telaListagemCursos()
            
        with aba_cadastro:
            telaCadastroCurso()
