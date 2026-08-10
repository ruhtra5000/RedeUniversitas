from html import escape
import streamlit as st

# Função para renderizar a página inicial com o nome do usuário
def renderizarHome(nome: str):
    aplicarEstiloHome()
    st.html('<span class="hv-page-marker"></span>')

    st.html(
        f"""
        <section class="hv-home">
            <div class="hv-home-eyebrow">REDE UNIVERSITAS</div>
            <h1 class="hv-home-title">
                Bem-vindo de volta,
                <span class="hv-home-name">{escape(nome)}</span>
            </h1>
            <p class="hv-home-description">
                Acesse pelo menu lateral os recursos acadêmicos,
                financeiros e administrativos disponíveis para o seu perfil.
            </p>
            <div class="hv-home-modules">
                <span class="hv-home-module">Gestão acadêmica</span>
                <span class="hv-home-module">Serviços financeiros</span>
                <span class="hv-home-module">Operações institucionais</span>
            </div>
        </section>
        """
    )

# Função para aplicar o estilo CSS personalizado na página inicial
def aplicarEstiloHome():
    st.html(
        """
        <style>
        [data-testid="stMainBlockContainer"]:has(.hv-page-marker) {
            width: 100%;
            max-width: 1180px !important;
            margin-right: auto !important;
            margin-left: auto !important;
            padding-top: 4.25rem !important;
            padding-right: 2.5rem !important;
            padding-bottom: 4rem !important;
            padding-left: 2.5rem !important;
        }

        .hv-page-marker {
            display: none;
        }

        [data-testid="stElementContainer"]:has(.hv-page-marker) {
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        .hv-home {
            position: relative;
            overflow: hidden;
            margin-top: 0.4rem;
            padding: 2.2rem 2.35rem;
            background:
                radial-gradient(
                    circle at 88% 8%,
                    rgba(196, 154, 74, 0.13),
                    transparent 26%
                ),
                linear-gradient(
                    135deg,
                    rgba(12, 31, 54, 0.99),
                    rgba(6, 17, 31, 0.99)
                );
            border: 1px solid rgba(148, 163, 184, 0.17);
            border-left: 3px solid #C49A4A;
            border-radius: 16px;
            box-shadow: 0 20px 55px rgba(0, 0, 0, 0.19);
        }

        .hv-home::after {
            content: "";
            position: absolute;
            top: -70px;
            right: -70px;
            width: 210px;
            height: 210px;
            border: 1px solid rgba(196, 154, 74, 0.11);
            border-radius: 50%;
        }

        .hv-home-eyebrow {
            color: #8190A4;
            font-size: 0.67rem;
            font-weight: 800;
            letter-spacing: 0.11em;
            text-transform: uppercase;
        }

        .hv-home-title {
            max-width: 780px;
            margin: 0.45rem 0 0;
            color: #F4F7FB;
            font-size: 2.35rem;
            font-weight: 790;
            letter-spacing: -0.04em;
            line-height: 1.08;
        }

        .hv-home-name {
            color: #E2C57F;
        }

        .hv-home-description {
            max-width: 680px;
            margin-top: 0.72rem;
            color: #93A1B3;
            font-size: 0.9rem;
            line-height: 1.55;
        }

        .hv-home-modules {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 1.35rem;
        }

        .hv-home-module {
            padding: 0.42rem 0.65rem;
            color: #B8C4D2;
            background: rgba(5, 13, 24, 0.48);
            border: 1px solid rgba(148, 163, 184, 0.14);
            border-radius: 8px;
            font-size: 0.68rem;
            font-weight: 650;
        }

        @media (max-width: 900px) {
            [data-testid="stMainBlockContainer"]:has(.hv-page-marker) {
                padding-right: 1rem !important;
                padding-left: 1rem !important;
            }

            .hv-home {
                padding: 1.5rem;
            }

            .hv-home-title {
                font-size: 1.8rem;
            }
        }
        </style>
        """
    )