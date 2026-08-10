from html import escape
import streamlit as st

# Função para exibir o cabeçalho da página com categoria, título, descrição e ícone
def cabecalhoPagina(categoria, titulo, descricao, icone):
    st.html(f"""
        <div class="ru-page-header">
            <div class="ru-page-icon">
                {escape(icone)}
            </div>

            <div>
                <div class="ru-page-eyebrow">
                    {escape(categoria)}
                </div>

                <h1 class="ru-page-title">
                    {escape(titulo)}
                </h1>

                <p class="ru-page-description">
                    {escape(descricao)}
                </p>
            </div>
        </div>
        """)

# Função para obter as iniciais de um nome completo
def obterIniciais(nome):
    partes = str(nome or "").strip().split()

    if not partes:
        return "?"

    if len(partes) == 1:
        return partes[0][:2].upper()

    return f"{partes[0][0]}{partes[-1][0]}".upper()

# Função para exibir um campo de identidade com rótulo e valor
def campoIdentidade(rotulo, valor):
    valorExibido = "Não informado" if valor in (None, "") else str(valor)

    st.html(f"""
        <div class="ru-field">
            <div class="ru-field-label">
                {escape(str(rotulo))}
            </div>

            <div class="ru-field-value">
                {escape(valorExibido)}
            </div>
        </div>
        """)
    
# Identidade visual da Rede Universitas
def temaRedeUniversitas():
    st.markdown(
        """
        <style>
        :root {
            --ru-background: #050B16;
            --ru-surface: #091426;
            --ru-surface-light: #0D1C32;
            --ru-surface-hover: #11233D;

            --ru-blue: #0B315F;
            --ru-blue-light: #174B82;

            --ru-gold: #C49A4A;
            --ru-gold-light: #E0BC70;
            --ru-gold-soft: rgba(196, 154, 74, 0.12);

            --ru-text: #F5F7FA;
            --ru-text-soft: #A8B4C5;
            --ru-border: rgba(148, 163, 184, 0.14);
        }

        html,
        body,
        [class*="css"] {
            font-family:
                Inter,
                "Segoe UI",
                Arial,
                sans-serif;
        }

        .stApp {
            color: var(--ru-text);
            background:
                radial-gradient(
                    circle at 88% 4%,
                    rgba(23, 75, 130, 0.22),
                    transparent 25%
                ),
                radial-gradient(
                    circle at 20% 90%,
                    rgba(196, 154, 74, 0.07),
                    transparent 25%
                ),
                var(--ru-background);
        }

        [data-testid="stAppViewContainer"] {
            background: transparent;
        }

        [data-testid="stHeader"] {
            background: rgba(5, 11, 22, 0.82);
            backdrop-filter: blur(12px);
        }

        [data-testid="stMainBlockContainer"] {
            width: 100%;
            max-width: 1180px;
            padding: 2rem 2.8rem 4rem;
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #081B35 0%,
                    #061326 100%
                );
            border-right: 1px solid rgba(196, 154, 74, 0.22);
        }

        [data-testid="stSidebar"] * {
            color: #EAF0F7;
        }

        [data-testid="stSidebarNav"] a {
            margin: 2px 10px;
            border-radius: 9px;
            transition: 160ms ease;
        }

        [data-testid="stSidebarNav"] a:hover {
            background: rgba(196, 154, 74, 0.10);
        }

        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background:
                linear-gradient(
                    90deg,
                    #C49A4A,
                    #D6AF62
                ) !important;
        }

        [data-testid="stSidebarNav"]
        a[aria-current="page"] * {
            color: #07172C !important;
            font-weight: 700 !important;
        }

        .ru-page-header {
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            gap: 1.25rem;

            padding: 1.6rem 1.8rem;
            margin: 0.7rem 0 1.4rem;

            background:
                linear-gradient(
                    115deg,
                    rgba(13, 28, 50, 0.98),
                    rgba(8, 20, 38, 0.96)
                );

            border: 1px solid var(--ru-border);
            border-left: 4px solid var(--ru-gold);
            border-radius: 18px;

            box-shadow:
                0 20px 45px rgba(0, 0, 0, 0.22);
        }

        .ru-page-header::after {
            content: "";
            position: absolute;
            width: 230px;
            height: 230px;
            right: -85px;
            top: -125px;
            border-radius: 50%;
            background: rgba(196, 154, 74, 0.07);
        }

        .ru-page-icon {
            width: 60px;
            height: 60px;
            flex: 0 0 60px;

            display: flex;
            align-items: center;
            justify-content: center;

            font-size: 1.65rem;

            color: #07172C;
            background:
                linear-gradient(
                    145deg,
                    var(--ru-gold-light),
                    var(--ru-gold)
                );

            border-radius: 16px;

            box-shadow:
                0 8px 24px rgba(196, 154, 74, 0.18);
        }

        .ru-page-eyebrow {
            margin-bottom: 0.25rem;
            color: var(--ru-gold-light);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.13em;
            text-transform: uppercase;
        }

        .ru-page-title {
            margin: 0;
            color: var(--ru-text);
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: -0.035em;
        }

        .ru-page-description {
            margin: 0.35rem 0 0;
            color: var(--ru-text-soft);
            font-size: 0.94rem;
        }

        .ru-toolbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;

            margin: 1.25rem 0 0.8rem;
            padding: 0.9rem 1.1rem;

            color: var(--ru-text-soft);
            background: rgba(9, 20, 38, 0.66);

            border: 1px solid var(--ru-border);
            border-radius: 13px;
        }

        .ru-toolbar-title {
            color: var(--ru-text);
            font-weight: 700;
        }

        .ru-count-badge,
        .ru-campus-badge,
        .ru-status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;

            padding: 0.38rem 0.72rem;

            color: var(--ru-gold-light);
            background: var(--ru-gold-soft);

            border: 1px solid rgba(196, 154, 74, 0.25);
            border-radius: 999px;

            font-size: 0.78rem;
            font-weight: 700;
        }

        .ru-count-dot {
            width: 7px;
            height: 7px;
            background: var(--ru-gold);
            border-radius: 50%;
            box-shadow: 0 0 10px rgba(196, 154, 74, 0.55);
        }

        .ru-hidden-marker {
            display: none;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:
        has(.ru-record-marker) {
            margin-bottom: 0.65rem;

            background:
                linear-gradient(
                    110deg,
                    rgba(13, 28, 50, 0.96),
                    rgba(9, 20, 38, 0.96)
                );

            border: 1px solid var(--ru-border) !important;
            border-radius: 15px !important;

            box-shadow:
                0 8px 24px rgba(0, 0, 0, 0.12);

            transition:
                border-color 160ms ease,
                transform 160ms ease,
                background 160ms ease;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:
        has(.ru-record-marker):hover {
            background: var(--ru-surface-hover);
            border-color: rgba(196, 154, 74, 0.43) !important;
            transform: translateY(-2px);
        }

        .ru-person {
            display: flex;
            align-items: center;
            gap: 0.85rem;
        }

        .ru-avatar {
            width: 43px;
            height: 43px;
            flex: 0 0 43px;

            display: flex;
            align-items: center;
            justify-content: center;

            color: #07172C;
            background:
                linear-gradient(
                    145deg,
                    var(--ru-gold-light),
                    var(--ru-gold)
                );

            border-radius: 12px;

            font-size: 0.84rem;
            font-weight: 900;
        }

        .ru-person-name {
            color: var(--ru-text);
            font-size: 0.95rem;
            font-weight: 750;
        }

        .ru-person-role {
            margin-top: 0.15rem;
            color: var(--ru-text-soft);
            font-size: 0.76rem;
        }

        .ru-data-label {
            margin-bottom: 0.22rem;
            color: #738198;
            font-size: 0.66rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .ru-data-value {
            overflow: hidden;
            color: #DCE5F0;
            font-size: 0.88rem;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .ru-profile-card {
            display: flex;
            align-items: center;
            gap: 1.1rem;

            margin: 1.1rem 0;
            padding: 1.35rem 1.5rem;

            background:
                linear-gradient(
                    105deg,
                    rgba(14, 31, 55, 0.98),
                    rgba(9, 20, 38, 0.96)
                );

            border: 1px solid var(--ru-border);
            border-left: 4px solid var(--ru-gold);
            border-radius: 16px;
        }

        .ru-profile-avatar {
            width: 62px;
            height: 62px;
            flex: 0 0 62px;

            display: flex;
            align-items: center;
            justify-content: center;

            color: #07172C;
            background:
                linear-gradient(
                    145deg,
                    var(--ru-gold-light),
                    var(--ru-gold)
                );

            border-radius: 17px;

            font-size: 1.05rem;
            font-weight: 900;
        }

        .ru-profile-content {
            flex: 1;
        }

        .ru-profile-name {
            margin: 0.18rem 0;
            color: var(--ru-text);
            font-size: 1.35rem;
            font-weight: 800;
        }

        .ru-profile-meta {
            color: var(--ru-text-soft);
            font-size: 0.84rem;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:
        has(.ru-detail-marker),
        [data-testid="stVerticalBlockBorderWrapper"]:
        has(.ru-form-section-marker) {
            background: rgba(9, 20, 38, 0.88);
            border: 1px solid var(--ru-border) !important;
            border-radius: 16px !important;
        }

        .ru-section-title {
            margin-bottom: 1rem;
            color: var(--ru-text);
            font-size: 1rem;
            font-weight: 800;
        }

        .ru-section-title span {
            margin-right: 0.45rem;
            color: var(--ru-gold);
        }

        .ru-field {
            min-height: 68px;
            padding: 0.75rem 0.9rem;

            background: rgba(5, 11, 22, 0.58);

            border: 1px solid rgba(148, 163, 184, 0.12);
            border-radius: 11px;
        }

        .ru-field-label {
            margin-bottom: 0.28rem;
            color: #77869B;
            font-size: 0.67rem;
            font-weight: 800;
            letter-spacing: 0.07em;
            text-transform: uppercase;
        }

        .ru-field-value {
            color: #EDF2F7;
            font-size: 0.9rem;
            font-weight: 650;
        }

        [data-testid="stForm"] {
            padding: 1.3rem;

            background: rgba(9, 20, 38, 0.85);

            border: 1px solid var(--ru-border) !important;
            border-radius: 16px !important;
        }

        [data-baseweb="input"] > div,
        [data-baseweb="select"] > div {
            color: var(--ru-text) !important;
            background: #07111F !important;

            border: 1px solid #263750 !important;
            border-radius: 10px !important;
        }

        [data-baseweb="input"] input {
            color: var(--ru-text) !important;
            -webkit-text-fill-color: var(--ru-text) !important;
        }

        [data-baseweb="input"]:focus-within,
        [data-baseweb="select"]:focus-within {
            border-radius: 10px;
            box-shadow:
                0 0 0 2px rgba(196, 154, 74, 0.30) !important;
        }

        [data-testid="stTextInput"] label,
        [data-testid="stSelectbox"] label {
            color: #C5D0DE !important;
            font-weight: 650 !important;
        }

        [data-testid="stBaseButton-primary"] {
            color: #07172C !important;
            background:
                linear-gradient(
                    135deg,
                    var(--ru-gold-light),
                    var(--ru-gold)
                ) !important;

            border: 1px solid var(--ru-gold) !important;
            border-radius: 10px !important;

            font-weight: 800 !important;
        }

        [data-testid="stBaseButton-primary"]:hover {
            color: #07172C !important;
            border-color: #F0D28B !important;

            box-shadow:
                0 7px 20px rgba(196, 154, 74, 0.20);
        }

        [data-testid="stBaseButton-secondary"] {
            color: #DDE6F1 !important;
            background: rgba(13, 28, 50, 0.72) !important;

            border: 1px solid #30425C !important;
            border-radius: 10px !important;

            font-weight: 650 !important;
        }

        [data-testid="stBaseButton-secondary"]:hover {
            color: var(--ru-gold-light) !important;
            background: rgba(196, 154, 74, 0.09) !important;
            border-color: var(--ru-gold) !important;
        }

        [data-testid="stAlert"] {
            color: var(--ru-text);
            border-radius: 12px;
        }

        [data-testid="stToast"] {
            color: var(--ru-text);
            background: var(--ru-surface-light);
            border-left: 4px solid var(--ru-gold);
        }

        div[data-testid="InputInstructions"] {
            display: none;
        }

        @media (max-width: 800px) {
            [data-testid="stMainBlockContainer"] {
                padding: 1rem;
            }

            .ru-page-header {
                padding: 1.2rem;
            }

            .ru-page-title {
                font-size: 1.5rem;
            }

            .ru-page-icon {
                width: 50px;
                height: 50px;
                flex-basis: 50px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

