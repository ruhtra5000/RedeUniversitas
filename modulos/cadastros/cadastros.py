import streamlit as st
from modulos.rotas import ROTA_CADASTRO_ALUNO, ROTA_CADASTRO_PROFESSOR, ROTA_CADASTRO_CURSO, ROTA_CADASTRO_DISCIPLINA, ROTA_CADASTRO_TURMA

def telaCadastros():
    placeholder_principal = st.empty()

    with placeholder_principal.container():
        st.title("🗂️ Central de Cadastros")
        st.caption("Selecione abaixo a categoria.")
        st.divider() 

        altura_cartao = 280 
        estilo_texto = "height: 100px; margin-bottom: 0px;"
        estilo_titulo = "white-space: nowrap; margin-bottom: 15px;"

        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>🎓 Alunos</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Cadastro de novos discentes, dados pessoais, contatos e vínculos.</div>", unsafe_allow_html=True)
                aluno_btn = st.button("Acessar", key="btn_aluno", use_container_width=True)

        with col2:
            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>👨‍🏫 Professores</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Cadastro de docentes, dados pessoais e campus.</div>", unsafe_allow_html=True)
                prof_btn = st.button("Acessar", key="btn_prof", use_container_width=True)

        with col3:
            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>📚 Cursos</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Gestão de cursos oferecidos, modalidades, durações e mensalidades.</div>", unsafe_allow_html=True)
                curso_btn = st.button("Acessar", key="btn_curso", use_container_width=True)

        st.write("")
        _espaco_esq, col4, col5, _espaco_dir = st.columns([1, 2, 2, 1])

        with col4:
            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>📘 Disciplinas</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Cadastro de matérias, carga horária e requisitos.</div>", unsafe_allow_html=True)
                disc_btn = st.button("Acessar", key="btn_disc", use_container_width=True)

        with col5:
            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>🏫 Turmas</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Criação de turmas, definição de semestre, disciplina e professores.</div>", unsafe_allow_html=True)
                turma_btn = st.button("Acessar", key="btn_turma", use_container_width=True)

    rota_destino = None
    if aluno_btn: rota_destino = ROTA_CADASTRO_ALUNO
    if prof_btn: rota_destino = ROTA_CADASTRO_PROFESSOR
    if curso_btn: rota_destino = ROTA_CADASTRO_CURSO
    if disc_btn: rota_destino = ROTA_CADASTRO_DISCIPLINA
    if turma_btn: rota_destino = ROTA_CADASTRO_TURMA

    if rota_destino:
        placeholder_principal.empty() 
        st.session_state.pagina = rota_destino
        st.rerun()