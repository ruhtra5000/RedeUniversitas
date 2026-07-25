import streamlit as st
from modulos.pages.home_page import telaHome
from modulos.cadastros.pages.cadastros_page import telaCadastros
from modulos.cadastros.pages.aluno_page import telaCadastroAluno
from modulos.cadastros.pages.professor_page import telaCadastroProfessor
from modulos.cadastros.pages.curso_page import telaCadastroCurso
from modulos.cadastros.pages.disciplina_page import telaCadastroDisciplina
from modulos.cadastros.pages.turma_page import telaCadastroTurma
from modulos.cadastros.pages.almoxarife_page import telaCadastroAlmoxarife
from modulos.cadastros.pages.bolsa_page import telaCadastroBolsa
from modulos.cadastros.pages.campus_page import telaCadastroCampus
from modulos.cadastros.pages.compra_page import telaCadastroCompra
from modulos.cadastros.pages.financeiro_page import telaCadastroFinanceiro
from modulos.cadastros.pages.fornecedor_page import telaCadastroFornecedor
from modulos.cadastros.pages.matricula_page import telaCadastroMatricula

def get_navigation():
    # Páginas principais
    home_page = st.Page(telaHome, title="Página Inicial", icon=":material/home:", default=True, url_path="home")
    cadastros_page = st.Page(telaCadastros, title="Central de Cadastros", icon=":material/folder:", url_path="cadastros")
    
    # Subpáginas de Cadastro
    cadastro_aluno = st.Page(telaCadastroAluno, title="Aluno", url_path="cadastro_aluno")
    cadastro_prof = st.Page(telaCadastroProfessor, title="Professor", url_path="cadastro_professor")
    cadastro_curso = st.Page(telaCadastroCurso, title="Curso", url_path="cadastro_curso")
    cadastro_disc = st.Page(telaCadastroDisciplina, title="Disciplina", url_path="cadastro_disciplina")
    cadastro_turma = st.Page(telaCadastroTurma, title="Turma", url_path="cadastro_turma")
    
    # Cadastros extras
    cadastro_almoxarife = st.Page(telaCadastroAlmoxarife, title="Almoxarife", url_path="cadastro_almoxarife")
    cadastro_bolsa = st.Page(telaCadastroBolsa, title="Bolsa", url_path="cadastro_bolsa")
    cadastro_campus = st.Page(telaCadastroCampus, title="Campus", url_path="cadastro_campus")
    cadastro_compra = st.Page(telaCadastroCompra, title="Compra", url_path="cadastro_compra")
    cadastro_financeiro = st.Page(telaCadastroFinanceiro, title="Financeiro", url_path="cadastro_financeiro")
    cadastro_fornecedor = st.Page(telaCadastroFornecedor, title="Fornecedor", url_path="cadastro_fornecedor")
    cadastro_matricula = st.Page(telaCadastroMatricula, title="Matrícula", url_path="cadastro_matricula")
    
    # Estrutura do menu lateral
    pages = {
        "Menu Principal": [
            home_page,
            cadastros_page,
        ],
        "Formulários de Cadastro": [
            cadastro_aluno,
            cadastro_prof,
            cadastro_curso,
            cadastro_disc,
            cadastro_turma,
            cadastro_almoxarife,
            cadastro_bolsa,
            cadastro_campus,
            cadastro_compra,
            cadastro_financeiro,
            cadastro_fornecedor,
            cadastro_matricula
        ]
    }
    return pages