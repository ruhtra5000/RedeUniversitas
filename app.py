import streamlit as st

from modulos.cadastros.campus import telaCadastroCampus
from modulos.home import telaHome
from modulos.cadastros.cadastros import telaCadastros

if "pagina" not in st.session_state:
    st.session_state.pagina = "home"

match st.session_state.pagina:
    case "home":
        telaHome()

    case "cadastro":
        telaCadastroCampus()

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
