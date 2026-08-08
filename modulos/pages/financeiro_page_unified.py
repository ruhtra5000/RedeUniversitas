import streamlit as st
from modulos.listagem.listagem_financeiro_page import telaListagemFinanceiros
from modulos.cadastros.pages.financeiro_page import telaCadastroFinanceiro
from modulos.view.view_financeiro_page import telaViewFinanceiro

def tela_financeiro_unificada():
    # Verifica se há um ID na sessão solicitando a view
    consulta_id = st.session_state.get("consulta_financeiro_id") or st.session_state.get("financeiro_id")
    
    if consulta_id:
        telaViewFinanceiro()
    else:
        aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
        
        with aba_listagem:
            telaListagemFinanceiros()
            
        with aba_cadastro:
            telaCadastroFinanceiro()
