import streamlit as st
from modulos.listagem.listagem_produto_page import telaListagemProdutos
from modulos.cadastros.pages.estoque_page import telaCadastroEstoque
from modulos.view.view_produto_page import telaViewProduto

def tela_estoque_unificada():
    # Verifica se há um ID na sessão solicitando a view
    consulta_id = st.session_state.get("consulta_produto_id") or st.session_state.get("produto_id")
    
    if consulta_id:
        telaViewProduto()
    else:
        aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
        
        with aba_listagem:
            telaListagemProdutos()
            
        with aba_cadastro:
            telaCadastroEstoque()
