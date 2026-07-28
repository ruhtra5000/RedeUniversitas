from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from database.Conexao import SessionLocal
from database.entidades.Bolsa import Bolsa
from database.entidades.enums.StatusBolsa import StatusBolsa
from modulos.cadastros.bolsa import criarBolsa
from modulos.academico.academico_service import listarAlunos
import database.entidades

def telaCadastroBolsa():
    if "form_key_bolsa" not in st.session_state:
        st.session_state.form_key_bolsa = 0

    st.title("🏷️ Cadastro de Bolsa")
    st.caption("Preencha as informações abaixo para conceder uma bolsa a um aluno.")

    st.markdown(
        """
        <style>
        div[data-testid="InputInstructions"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.pop("cadastro_bolsa_realizado", False):
        st.toast("Bolsa cadastrada com sucesso!", icon="🎉")

    col1, _ = st.columns([1, 6])
    with col1:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import cadastros_page
            st.switch_page(cadastros_page)

    if "cache_alunos" not in st.session_state:
        st.session_state.cache_alunos = listarAlunos()

    lista_alunos = st.session_state.cache_alunos

    if not lista_alunos:
        st.warning(
            """
            ⚠️ Antes de cadastrar uma bolsa é necessário possuir:
            - Pelo menos **1 Aluno**
            """
        )

    with st.form(key=f"cadastro_bolsa_{st.session_state.form_key_bolsa}", border=False):
        
        with st.container(border=True):
            st.subheader("👤 Vínculo e Tipo de Bolsa")
            
            with st.container(horizontal=True):
                aluno_selecionado = st.selectbox(
                    "Aluno *",
                    options=lista_alunos if lista_alunos else [],
                    format_func=lambda a: a.pessoa.nome,
                    index=None,
                    placeholder="Selecione um aluno...",
                    disabled=not lista_alunos,
                    key=f"bolsa_aluno_{st.session_state.form_key_bolsa}"
                )
                tipo_bolsa = st.text_input(
                    "Tipo de Bolsa *",
                    placeholder="Ex.: Bolsa Mérito, Bolsa Atleta",
                    key=f"bolsa_tipo_{st.session_state.form_key_bolsa}"
                )

            with st.container(horizontal=True):
                percentual_desconto = st.number_input(
                    "Percentual de Desconto (0.0 a 1.0) *",
                    min_value=0.01,
                    max_value=1.00,
                    step=0.05,
                    format="%.2f",
                    help="1.0 equivale a 100% de bolsa.",
                    key=f"bolsa_perc_{st.session_state.form_key_bolsa}"
                )
                status_bolsa = st.selectbox(
                    "Status da Bolsa *",
                    options=list(StatusBolsa),
                    format_func=lambda s: s.name.title(),
                    key=f"bolsa_status_{st.session_state.form_key_bolsa}"
                )

        st.write("")

        with st.container(border=True):
            st.subheader("📅 Período de Vigência")

            with st.container(horizontal=True):
                data_inicio = st.date_input(
                    "Data de Início *",
                    format="DD/MM/YYYY",
                    key=f"bolsa_inicio_{st.session_state.form_key_bolsa}"
                )
                data_fim = st.date_input(
                    "Data de Término *",
                    format="DD/MM/YYYY",
                    key=f"bolsa_fim_{st.session_state.form_key_bolsa}"
                )

        st.write("")

        _, centro, _ = st.columns([2, 3, 2])
        with centro:
            cadastrar = st.form_submit_button(
                "💾 Cadastrar Bolsa", 
                type="primary", 
                use_container_width=True
            )

    if cadastrar:
        if not lista_alunos:
            st.error("Cadastre pelo menos um Aluno antes de continuar.")
        elif aluno_selecionado is None:
            st.error("Por favor, selecione um Aluno.")
        elif not tipo_bolsa.strip():
            st.error("Por favor, preencha o Tipo de Bolsa.")
        else:
            try:
                nova_bolsa = Bolsa(
                    aluno_id=aluno_selecionado.pessoa_id,
                    tipo_bolsa=tipo_bolsa.strip(),
                    percentual_desconto=percentual_desconto,
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    status=status_bolsa
                )
                
                criarBolsa(bolsa=nova_bolsa, aluno=aluno_selecionado)
                
                st.session_state.form_key_bolsa += 1 
                st.session_state["cadastro_bolsa_realizado"] = True
                
                st.rerun()
                
            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(str(e))