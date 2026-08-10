from sqlalchemy import select
import streamlit as st
from database.Conexao import SessionLocal
from database.entidades.Pessoa import Pessoa
from modulos.cadastros.mensalidade import geracaoAutomaticaMensalidade
from modulos.rotas import get_navigation
from modulos.temaRedeUniversitas import temaRedeUniversitas
from modulos.sidebar import (aplicarEstiloSidebar, renderizarLogoutSidebar, renderizarPerfilUsuario, renderizarTituloSecaoSidebar)

st.set_page_config(
    page_title="RedeUniversitas",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Aplicar tema personalizado da RedeUniversitas
temaRedeUniversitas()

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
            width="stretch",
        ):
            st.login()
            st.stop()
    
def verificarLogin():
    google_id = st.user.sub
    email = st.user.email

    with SessionLocal() as session:
        from sqlalchemy.orm import joinedload
        query = select(Pessoa).options(
            joinedload(Pessoa.professor),
            joinedload(Pessoa.almoxarife),
            joinedload(Pessoa.aluno),
            joinedload(Pessoa.financeiro)
        ).where(Pessoa.google_id == google_id)
        
        pessoa = session.execute(query).scalar_one_or_none()

        if pessoa == None:
            query = select(Pessoa).options(
                joinedload(Pessoa.professor),
                joinedload(Pessoa.almoxarife),
                joinedload(Pessoa.aluno),
                joinedload(Pessoa.financeiro)
            ).where(Pessoa.email == email)
            pessoaEmail = session.execute(query).scalar_one_or_none()

            if pessoaEmail != None:
                pessoaEmail.google_id = google_id
                session.commit()
                pessoa = pessoaEmail
            else:
                st.warning("E-mail não cadastrado!")
                st.logout()
                st.stop()
        
        if "roles" not in st.session_state:
            roles = []
            if pessoa.professor: 
                roles.append("PROFESSOR")
                # Verifica se é reitor de algum campus
                from database.entidades.Campus import Campus
                reitor_campus = session.execute(select(Campus).where(Campus.reitor_id == pessoa.id)).scalar_one_or_none()
                if reitor_campus:
                    roles.append("REITOR")

            if pessoa.almoxarife: roles.append("ALMOXARIFE")
            if pessoa.aluno: roles.append("ALUNO")
            if pessoa.financeiro: roles.append("FINANCEIRO")
            if pessoa.is_admin: roles.append("ADMIN")
            
            st.session_state.roles = roles
            st.session_state.pessoa_logada = pessoa.nome
            st.session_state.pessoa_id = pessoa.id

# Lógica de login
if not st.user.is_logged_in:
    telaLogin()
    st.stop()
else:
    verificarLogin() 
    # fica gerando mensagem de login toda hora 
    # (acho que dá pra juntar na parte de logica de paginas)

# Configuração das Rotas (ocultando a sidebar nativa)
nav_dict = get_navigation()
pg = st.navigation(nav_dict, position="hidden")

# Renderização do Perfil e Menu na Sidebar
with st.sidebar:
    aplicarEstiloSidebar()

    renderizarPerfilUsuario()

    with st.container(
        key="sidebar_menu",
    ):
        for section, pages in nav_dict.items():

            if section == "Edições (Oculto)":
                continue

            renderizarTituloSecaoSidebar(
                section
            )

            for page in pages:
                st.page_link(
                    page,
                    label=page.title,
                    icon=page.icon,
                )

    renderizarLogoutSidebar()

# Execução da página atual
pg.run()