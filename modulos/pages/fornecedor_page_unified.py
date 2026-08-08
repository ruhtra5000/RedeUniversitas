import streamlit as st
from modulos.listagem.listagem_fornecedor_page import telaListagemFornecedores
from modulos.cadastros.pages.fornecedor_page import telaCadastroFornecedor
from modulos.view.view_fornecedor_page import telaViewFornecedor

def tela_fornecedor_unificada():
    # Verifica se há um ID na sessão solicitando a view
    consulta_id = st.session_state.get("consulta_fornecedor_id")
    
    if consulta_id:
        telaViewFornecedor()
    else:
        aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
        
        with aba_listagem:
            telaListagemFornecedores()
            
        with aba_cadastro:
            telaCadastroFornecedor()
