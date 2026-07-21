from sqlalchemy import select
from modulos.utils.text_utils import *
import streamlit as st

from database.Conexao import SessionLocal
import database.entidades 
from database.entidades.Pessoa import Pessoa
from modulos.cadastros.mensalidade import geracaoAutomaticaMensalidade
from modulos.home import telaHome
from modulos.cadastros.cadastros import telaCadastros

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
    st.session_state.pagina = "home"

# Ícones e rotas da sidebar
nav_items = [
    {"id": "home", "label": "Página Inicial", "icon": ":material/home:", "view": telaHome},
    {"id": "cadastros", "label": "Cadastros", "icon": ":material/folder:", "view": telaCadastros},
    {"id": "academico", "label": "Acadêmico", "icon": ":material/school:", "view": None},
    {"id": "financeiro", "label": "Financeiro", "icon": ":material/money_bag:", "view": None},
    {"id": "almoxarifado", "label": "Almoxarifado", "icon": ":material/inventory_2:", "view": None},
    {"id": "relatorios", "label": "Relatórios", "icon": ":material/analytics:", "view": None},
]

st.sidebar.subheader("Navegação")
for item in nav_items:
    if st.sidebar.button(
        f"{item['icon']} {item['label']}",
        key=f"nav_{item['id']}",
        use_container_width=True,
        type="primary" if st.session_state.pagina == item["id"] else "secondary",
    ):
        st.session_state.pagina = item["id"]
        st.rerun()

st.sidebar.divider()

# Usuario e Logout
st.sidebar.text(f"Olá, {formata_primeiro_nome(st.user.name)}!")
if st.sidebar.button(":material/logout: Logout", use_container_width=True):
    st.logout()
    st.stop()

# Encontrar a página selecionada pela navegação
pagina_selecionada = (item for item in nav_items if item["id"] == st.session_state.pagina)

# Obtém o próximo item do generator, ou retorna a primeira página (home) se nenhuma for encontrada
pagina_atual = next(pagina_selecionada, nav_items[0])

# Verifica se a página selecionada possui uma view definida
if pagina_atual["view"] is not None:
    # Se houver, executa a função view associada à página
    pagina_atual["view"]()
else:
    # Caso contrário, exibe uma mensagem informando que a página está em desenvolvimento
    st.info(f"A página **{pagina_atual['label']}** ainda está em desenvolvimento.")