from html import escape
import streamlit as st
from modulos.utils.text_utils import formata_primeiro_nome

# Função para renderizar o perfil do usuário na barra lateral
def renderizarPerfilUsuario():
    nome_completo = st.session_state.get(
        "pessoa_logada",
        st.user.name,
    )

    nome_usuario = formata_primeiro_nome(nome_completo)

    if not nome_usuario:
        nome_usuario = "Usuário"

    inicial = nome_usuario[0].upper()

    roles = st.session_state.get(
        "roles",
        [],
    )

    nomes_roles = {
        "ADMIN": "Admin",
        "PROFESSOR": "Professor",
        "ALUNO": "Aluno",
        "REITOR": "Reitor",
        "ALMOXARIFE": "Almoxarife",
        "FINANCEIRO": "Financeiro",
    }

    cargos = " • ".join(
        nomes_roles.get(
            role,
            role.replace("_", " ").title(),
        )
        for role in roles
    )

    if not cargos:
        cargos = "Usuário"

    with st.container(
        key="sidebar_perfil",
    ):
        st.html(f"""
            <div class="ru-perfil">

                <div class="ru-avatar">
                    {escape(inicial)}
                </div>

                <div class="ru-perfil-conteudo">

                    <div class="ru-perfil-label">
                        Minha conta
                    </div>

                    <div
                        class="ru-perfil-nome"
                        title="{escape(nome_usuario)}"
                    >
                        {escape(nome_usuario)}
                    </div>

                    <div
                        class="ru-perfil-cargos"
                        title="{escape(cargos)}"
                    >
                        {escape(cargos)}
                    </div>

                </div>

            </div>
            """)

# Função para renderizar o título de uma seção na barra lateral
def renderizarTituloSecaoSidebar(titulo: str):
    st.html(f"""
        <div class="ru-menu-section">
            {escape(titulo)}
        </div>
        """)

# Função para renderizar o botão de logout na barra lateral
def renderizarLogoutSidebar():
    with st.container(
        key="sidebar_footer",
    ):
        if st.button(
            "Sair da conta",
            icon=":material/logout:",
            width="stretch",
            key="logout_sidebar",
        ):
            st.logout()
            st.stop()

# Função para aplicar estilo personalizado na barra lateral do Streamlit
def aplicarEstiloSidebar():
    st.html("""
        <style>

        section[data-testid="stSidebar"] {
            border-right: 1px solid rgba(148, 163, 184, 0.12);
        }

        section[data-testid="stSidebar"]
        div[data-testid="stSidebarUserContent"] {
            padding:
                1rem
                1rem
                0.8rem
                1rem;
        }

        section[data-testid="stSidebar"]
        div[data-testid="stSidebarUserContent"]
        > div[data-testid="stVerticalBlock"] {
            min-height: calc(100vh - 2rem);

            display: flex;
            flex-direction: column;

            gap: 0 !important;
        }

        .st-key-sidebar_perfil {
            margin: 0 !important;
            padding: 0 !important;
        }

        .st-key-sidebar_perfil
        div[data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }

        .ru-perfil {
            width: 100%;

            display: flex;
            align-items: center;

            gap: 0.7rem;

            padding:
                0.15rem
                0.1rem
                0.85rem
                0.1rem;

            box-sizing: border-box;

            border-bottom:
                1px solid rgba(148, 163, 184, 0.14);
        }

        .ru-avatar {
            width: 40px;
            height: 40px;

            min-width: 40px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 10px;

            background:
                linear-gradient(
                    145deg,
                    rgba(219, 174, 70, 0.16),
                    rgba(219, 174, 70, 0.07)
                );

            border:
                1px solid rgba(219, 174, 70, 0.34);

            color: #e1b64c;

            font-size: 0.9rem;
            font-weight: 800;

            box-shadow:
                inset 0 0 0 1px
                rgba(255, 255, 255, 0.015);
        }

        .ru-perfil-conteudo {
            flex: 1;
            min-width: 0;
        }

        .ru-perfil-label {
            margin-bottom: 0.12rem;

            color: #7594bb;

            font-size: 0.57rem;
            font-weight: 800;

            line-height: 1.15;

            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .ru-perfil-nome {
            max-width: 100%;

            color: #f4f7fb;

            font-size: 0.91rem;
            font-weight: 700;

            line-height: 1.2;

            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .ru-perfil-cargos {
            max-width: 100%;

            margin-top: 0.18rem;

            color: #8098b8;

            font-size: 0.63rem;
            font-weight: 500;

            line-height: 1.2;

            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .st-key-sidebar_menu {
            margin: 0 !important;

            padding:
                0.15rem
                0
                0
                0 !important;
        }

        .st-key-sidebar_menu
        > div[data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }

        .ru-menu-section {
            margin:
                0.8rem
                0
                0.25rem
                0;

            padding:
                0
                0.15rem;

            color: #eef3f8;

            font-size: 0.72rem;
            font-weight: 700;

            line-height: 1.2;
        }

        section[data-testid="stSidebar"]
        [data-testid="stPageLink"] {
            margin: 0 !important;
            padding: 0 !important;
        }

        section[data-testid="stSidebar"]
        [data-testid="stPageLink"] a {
            min-height: 2rem;

            margin: 0 !important;

            padding:
                0.30rem
                0.50rem !important;

            border-radius: 7px;

            transition:
                background-color 0.15s ease,
                color 0.15s ease;
        }

        section[data-testid="stSidebar"]
        [data-testid="stPageLink"] p {
            margin: 0;

            font-size: 0.76rem;
            font-weight: 500;
        }

        section[data-testid="stSidebar"]
        [data-testid="stPageLink"] svg {
            width: 1rem;
            height: 1rem;
        }

        .st-key-sidebar_footer {
            margin-top: auto !important;

            padding-top: 0.75rem !important;

            border-top:
                1px solid rgba(148, 163, 184, 0.14);
        }

        .st-key-sidebar_footer
        > div[data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }

        .st-key-sidebar_footer button {
            min-height: 2.25rem;

            background:
                rgba(148, 163, 184, 0.035) !important;

            border:
                1px solid
                rgba(148, 163, 184, 0.16) !important;

            color: #91a8c4 !important;

            box-shadow: none !important;

            transition:
                background-color 0.15s ease,
                border-color 0.15s ease,
                color 0.15s ease;
        }

        .st-key-sidebar_footer button:hover {
            background:
                rgba(148, 163, 184, 0.08) !important;

            border-color:
                rgba(148, 163, 184, 0.28) !important;

            color: #f3f6fa !important;
        }

        .st-key-sidebar_footer button p {
            font-size: 0.74rem;
            font-weight: 600;
        }
        
        section[data-testid="stSidebar"]
        ::-webkit-scrollbar {
            width: 5px;
        }

        section[data-testid="stSidebar"]
        ::-webkit-scrollbar-thumb {
            background:
                rgba(148, 163, 184, 0.22);

            border-radius: 10px;
        }

        section[data-testid="stSidebar"]
        ::-webkit-scrollbar-track {
            background: transparent;
        }

        </style>
        """)
