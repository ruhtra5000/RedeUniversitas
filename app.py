from sqlalchemy import select
import streamlit as st

from database.Conexao import SessionLocal
import database.entidades 
from database.entidades.Pessoa import Pessoa
from modulos.cadastros.mensalidade import geracaoAutomaticaMensalidade
from modulos.rotas import ROTA_HOME, get_rotas
from modulos.sidebar import renderizar_sidebar

st.set_page_config(
    page_title="RedeUniversitas",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Gerar mensalidades automaticamente
geracaoAutomaticaMensalidade()

# Funções de login
def telaLogin():
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        # TODO: colocar logo depois
        st.title("🎓 RedeUniversitas", text_alignment="center")
        st.divider()

        if st.button(
            "![Google](https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg) Entrar com Google",
            use_container_width=True,
        ):
            st.login()
            st.stop()
    
def verificarLogin():
    google_id = st.user.sub
    email = st.user.email

    with SessionLocal() as session:
        query = select(Pessoa).where(Pessoa.google_id == google_id)
        pessoa = session.execute(query).scalar_one_or_none()

        if pessoa == None:
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
    st.stop()
else:
    verificarLogin() 
    # fica gerando mensagem de login toda hora 
    # (acho que dá pra juntar na parte de logica de paginas)

# Lógica de paginas inicial (MUDAR)
if "pagina" not in st.session_state:
    st.session_state.pagina = ROTA_HOME

# Renderização da Sidebar
renderizar_sidebar()

# Renderização da Página Atual
view_atual = get_rotas().get(st.session_state.pagina)

if view_atual is not None:
    view_atual()
else:
    st.info(f"A página **{st.session_state.pagina}** ainda está em desenvolvimento!")