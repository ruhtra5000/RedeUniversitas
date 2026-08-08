import streamlit as st
from modulos.listagem.listagem_bolsa_page import telaListagemBolsas
from modulos.cadastros.pages.bolsa_page import telaCadastroBolsa

def tela_bolsa_unificada():
    aba_listagem, aba_cadastro = st.tabs([":material/assignment: Listagem", ":material/add: Novo Cadastro"])
    
    with aba_listagem:
        telaListagemBolsas()
        
    with aba_cadastro:
        telaCadastroBolsa()
