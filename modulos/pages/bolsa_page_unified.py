import streamlit as st
from modulos.listagem.listagem_bolsa_page import telaListagemBolsas
from modulos.cadastros.pages.bolsa_page import telaCadastroBolsa
from modulos.view.view_bolsa_page import telaViewBolsa

def tela_bolsa_unificada():
    # Verifica se há um ID na sessão solicitando a view
    consulta_id = st.session_state.get("consulta_bolsa_id") or st.session_state.get("bolsa_id")
    
    if consulta_id:
        telaViewBolsa()
    else:
        aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
        
        with aba_listagem:
            telaListagemBolsas()
            
        with aba_cadastro:
            telaCadastroBolsa()
