import streamlit as st

def telaCadastros():
    placeholder_principal = st.empty()

    with placeholder_principal.container():
        st.title("🗂️ Central de Cadastros")
        st.caption("Selecione abaixo a categoria.")
        st.divider() 

        altura_cartao = 280 
        estilo_texto = "height: 100px; margin-bottom: 0px;"
        estilo_titulo = "white-space: nowrap; margin-bottom: 15px;"

        # Container horizontal (uma linha) com 3
        with st.container(horizontal=True):
            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>🎓 Alunos</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Cadastro de novos discentes, dados pessoais, contatos e vínculos.</div>", unsafe_allow_html=True)
                aluno_btn = st.button("Acessar", key="btn_aluno", width="stretch")

            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>👨‍🏫 Professores</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Cadastro de docentes, dados pessoais e campus.</div>", unsafe_allow_html=True)
                prof_btn = st.button("Acessar", key="btn_prof", width="stretch")

            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>📚 Cursos</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Gestão de cursos oferecidos, modalidades, durações e mensalidades.</div>", unsafe_allow_html=True)
                curso_btn = st.button("Acessar", key="btn_curso", width="stretch")

        st.write("")

        with st.container(horizontal=True):
            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>📘 Disciplinas</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Cadastro de matérias, carga horária e requisitos.</div>", unsafe_allow_html=True)
                disc_btn = st.button("Acessar", key="btn_disc", width="stretch")

            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>🏫 Turmas</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Criação de turmas, definição de semestre, disciplina e professores.</div>", unsafe_allow_html=True)
                turma_btn = st.button("Acessar", key="btn_turma", width="stretch")

            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>🎓 Matrículas</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Matrícula de alunos nas turmas e checagem de pré-requisitos.</div>", unsafe_allow_html=True)
                matricula_btn = st.button("Acessar", key="btn_matricula", width="stretch")

        st.write("")
        
        with st.container(horizontal=True):
            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>🏢 Campus</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Criação das unidades e gerenciamento de seus caixas.</div>", unsafe_allow_html=True)
                campus_btn = st.button("Acessar", key="btn_campus", width="stretch")

            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>📦 Almoxarifes</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Cadastro de encarregados do estoque e almoxarifado.</div>", unsafe_allow_html=True)
                almoxarife_btn = st.button("Acessar", key="btn_almoxarife", width="stretch")

            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>🏷️ Bolsas</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Concessão de bolsas e descontos aos alunos.</div>", unsafe_allow_html=True)
                bolsa_btn = st.button("Acessar", key="btn_bolsa", width="stretch")

        st.write("")

        with st.container(horizontal=True):
            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>💼 Financeiros</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Cadastro de funcionários responsáveis pelos caixas.</div>", unsafe_allow_html=True)
                financeiro_btn = st.button("Acessar", key="btn_financeiro", width="stretch")

            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>🚚 Fornecedores</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Registros de parceiros e fornecedores de produtos.</div>", unsafe_allow_html=True)
                fornecedor_btn = st.button("Acessar", key="btn_fornecedor", width="stretch")

            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>🛒 Compras</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Registro de entrada de produtos e geração de contas a pagar.</div>", unsafe_allow_html=True)
                compra_btn = st.button("Acessar", key="btn_compra", width="stretch")

        st.write("")

        with st.container(horizontal=True):
            with st.container(height=altura_cartao, border=True):
                st.markdown(f"<h3 style='{estilo_titulo}'>📦 Estoque (Produto)</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='{estilo_texto}'>Cadastro de produtos para o estoque e inventário.</div>", unsafe_allow_html=True)
                estoque_btn = st.button("Acessar", key="btn_estoque", width="stretch")

            st.container(height=altura_cartao, border=False)
            st.container(height=altura_cartao, border=False)


    from modulos.rotas import (
        cadastro_aluno, cadastro_prof, cadastro_curso, cadastro_disc, cadastro_turma,
        cadastro_almoxarife, cadastro_bolsa, cadastro_campus, cadastro_compra,
        cadastro_financeiro, cadastro_fornecedor, cadastro_matricula, cadastro_estoque
    )
    
    rota_destino = None
    if aluno_btn: rota_destino = cadastro_aluno
    if prof_btn: rota_destino = cadastro_prof
    if curso_btn: rota_destino = cadastro_curso
    if disc_btn: rota_destino = cadastro_disc
    if turma_btn: rota_destino = cadastro_turma
    if matricula_btn: rota_destino = cadastro_matricula
    if campus_btn: rota_destino = cadastro_campus
    if almoxarife_btn: rota_destino = cadastro_almoxarife
    if bolsa_btn: rota_destino = cadastro_bolsa
    if financeiro_btn: rota_destino = cadastro_financeiro
    if fornecedor_btn: rota_destino = cadastro_fornecedor
    if compra_btn: rota_destino = cadastro_compra
    if estoque_btn: rota_destino = cadastro_estoque

    if rota_destino:
        st.switch_page(rota_destino)