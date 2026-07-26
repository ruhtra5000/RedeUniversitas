from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from validate_docbr.CNPJ import CNPJ
from database.Conexao import SessionLocal
from database.entidades.Caixa import Caixa
from database.entidades.Campus import Campus
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
import database.entidades
from modulos.cadastros.campus import criarCampus

def telaCadastroCampus():
    st.title("Cadastro de Campus")

    with st.form("form_campus"):
        cnpj = st.number_input(
            label="CNPJ",
            step=1
        )
        nome = st.text_input("Nome")
        email = st.text_input("E-mail")
        telefone = st.text_input("Telefone")

        enviar = st.form_submit_button("Salvar")

    if enviar:
        campus = Campus(
            cnpj = cnpj,
            nome = nome,
            email = email,
            telefone = telefone
        )

        criarCampus(campus)

        st.write("Campus cadastrado!")