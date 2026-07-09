import streamlit as st

from database.Conexao import SessionLocal
from database.entidades.Campus import Campus

# Aqui ficaria a parte de interface
st.write("Cadastro de Campus")


# Aqui seria a "camada de serviço", onde voce pode pegar 
# os dados da interface e/ou fazer alguma checagem de regra de negocio 
def criarCampus():
    dado1 = "nome"
    dado2 = "cnpj"

    campus = Campus(
        nome = dado1,
        cnpj = dado2,
        # ...
    )

    dbCriarCampus(campus)


# Aqui seria a camada de dados (somente ela deve interagir diretamente com o banco)
def dbCriarCampus(campus: Campus):
    with SessionLocal() as session:
        session.add(campus)
        session.commit()