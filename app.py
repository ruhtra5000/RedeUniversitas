from sqlalchemy import select
import streamlit as st

from database.Conexao import SessionLocal
import database.entidades 
from database.entidades.Pessoa import Pessoa
from modulos.cadastros.campus import telaCadastroCampus
from modulos.home import telaHome
from modulos.cadastros.cadastros import telaCadastros

# Funções de login
def telaLogin():
    st.title("Login")

    if not st.user.is_logged_in:
        if st.button("Login com Google"):
            st.login()
            st.stop()
    
def verificarLogin():
    google_id = st.user.sub
    email = st.user.email

    with SessionLocal() as session:
        query = select(Pessoa).where(Pessoa.google_id == google_id)
        pessoa = session.execute(query).scalar_one_or_none()

        if pessoa != None:
            st.success("Usuário logado.")

        else:
            query = select(Pessoa).where(Pessoa.email == email)
            pessoaEmail = session.execute(query).scalar_one_or_none()

            if pessoaEmail != None:
                pessoaEmail.google_id = google_id
                session.commit()
            else:
                st.warning("E-mail não cadastrado!")
                st.logout()

# Lógica de login
if not st.user.is_logged_in:
    telaLogin()
else:
    verificarLogin() 
    # fica gerando mensagem de login toda hora 
    # (acho que dá pra juntar na parte de logica de paginas)
    if st.button("Logout"):
        st.logout()

# Lógica de paginas inicial (MUDAR)
if "pagina" not in st.session_state:
    st.session_state.pagina = "" 

match st.session_state.pagina:
    case "home":
        telaHome()

    case "cadastro":
        telaCadastroCampus()

# Sidebar paia
pagina = st.sidebar.radio(
    "Módulos",
    [
        "Home",
        "Cadastros",
        "Acadêmico",
        "Financeiro",
        "Almoxarifado",
        "Relatórios"
    ]
)
