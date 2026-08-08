import streamlit as st
from modulos.listagem.listagem_bolsa_page import telaListagemBolsas
from modulos.cadastros.pages.bolsa_page import telaCadastroBolsa
from modulos.view.view_bolsa_page import view_bolsa

def tela_bolsa_unificada():
    # Verifica se há um ID na sessão solicitando a view
    consulta_id = st.session_state.get("consulta_bolsa_id")
    
    if consulta_id:
        view_bolsa()
    else:
        aba_listagem, aba_cadastro = st.tabs(["📋 Listagem", "➕ Novo Cadastro"])
        
        with aba_listagem:
            telaListagemBolsas()
            
        with aba_cadastro:
            telaCadastroBolsa()
