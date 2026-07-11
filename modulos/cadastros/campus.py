from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from validate_docbr.CNPJ import CNPJ

from database.Conexao import SessionLocal
from database.entidades.Campus import Campus
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
import database.entidades

# Aqui ficaria a parte de interface
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


# Aqui seria a "camada de serviço", onde voce pode pegar 
# os dados da interface e/ou fazer alguma validação de regra de negocio 
def criarCampus(campus: Campus):
    try:
        if not CNPJ().validate(campus.cnpj):
            raise Exception("O CNPJ disponibilizado não é válido.")
        
        if campus.email != "":
            if not validarEmail(campus.email):
                raise Exception("O E-mail disponibilizado não é válido.")
            
        if campus.telefone != "":
            if not validarTelefone(campus.telefone):
                raise Exception("O telefone disponibilizado não é válido.")

        dbCriarCampus(campus)

    except SQLAlchemyError:
        raise


# Aqui seria a camada de dados (somente ela deve interagir diretamente com o banco)
def dbCriarCampus(campus: Campus):
    with SessionLocal() as session:
        try:
            session.add(campus)
            session.commit()
        
        except SQLAlchemyError:
            raise