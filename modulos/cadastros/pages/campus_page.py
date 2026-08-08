from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from database.Conexao import SessionLocal
from database.entidades.Caixa import Caixa
from database.entidades.Campus import Campus
from modulos.cadastros.campus import criarCampus
import database.entidades

def telaCadastroCampus():
    if "form_key_campus" not in st.session_state:
        st.session_state.form_key_campus = 0


    st.title(":material/domain_add: Cadastro de Campus")
    st.caption("Preencha as informações abaixo para cadastrar um novo campus.")

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

    if st.session_state.pop("cadastro_campus_realizado", False):
        st.toast("Campus cadastrado com sucesso!", icon=":material/check:")

    with st.form(key=f"cadastro_campus_{st.session_state.form_key_campus}", border=False):
        
        with st.container():
            st.subheader("Dados da Unidade")
            
            with st.container(horizontal=True):
                nome = st.text_input(
                    "Nome do Campus *",
                    placeholder="Ex.: Campus Central",
                    key=f"campus_nome_{st.session_state.form_key_campus}"
                )
                cnpj = st.text_input(
                    "CNPJ *",
                    placeholder="Somente números",
                    key=f"campus_cnpj_{st.session_state.form_key_campus}"
                )
                valor_caixa = st.number_input(
                    "Valor Inicial do Caixa (R$)",
                    min_value=0.0,
                    step=100.0,
                    format="%.2f",
                    key=f"campus_caixa_{st.session_state.form_key_campus}"
                )

        with st.container():
            with st.container(horizontal=True):
                cidade = st.text_input(
                    "Cidade *",
                    placeholder="Ex.: São Paulo",
                    key=f"campus_cidade_{st.session_state.form_key_campus}"
                )
                estado = st.text_input(
                    "Estado *",
                    placeholder="Ex.: SP",
                    max_chars=2,
                    key=f"campus_estado_{st.session_state.form_key_campus}"
                )

        with st.container():
            c3, c4 = st.columns(2)
            with c3:
                email = st.text_input(
                    "E-mail *",
                    placeholder="contato@campus.com",
                    key=f"campus_email_{st.session_state.form_key_campus}"
                )
            with c4:
                telefone = st.text_input(
                    "Telefone",
                    placeholder="Opcional",
                    key=f"campus_telefone_{st.session_state.form_key_campus}"
                )

        st.write("")

        _, centro, _ = st.columns([2, 3, 2])
        with centro:
            cadastrar = st.form_submit_button(
                "Cadastrar Campus", 
                type="primary", 
                width="stretch"
            )

    if cadastrar:
        if not nome.strip() or not cnpj.strip() or not email.strip():
            st.error("Por favor, preencha todos os campos obrigatórios (Nome, CNPJ e E-mail).")
        else:
            try:
                import re
                novo_campus = Campus(
                    cnpj=re.sub(r'\D', '', cnpj),
                    nome=nome.strip(),
                    email=email.strip(),
                    telefone=telefone.strip() if telefone.strip() != "" else None
                )
                
                criarCampus(campus=novo_campus, valorInicialCaixa=valor_caixa)
                
                st.session_state.form_key_campus += 1
                st.session_state.pop("cache_campus", None) 
                st.session_state["cadastro_campus_realizado"] = True
                
                st.rerun()
                
            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(str(e))