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
from modulos.cadastros.pages.estoque_page import telaCadastroEstoque

# Páginas principais
home_page = st.Page(telaHome, title="Página Inicial", icon=":material/home:", default=True, url_path="home")
cadastros_page = st.Page(telaCadastros, title="Central de Cadastros", icon=":material/folder:", url_path="cadastros")

# Subpáginas de Cadastro
cadastro_aluno = st.Page(telaCadastroAluno, title="Aluno", icon=":material/person_add:", url_path="cadastro_aluno")
cadastro_prof = st.Page(telaCadastroProfessor, title="Professor", icon=":material/group_add:", url_path="cadastro_professor")
cadastro_curso = st.Page(telaCadastroCurso, title="Curso", icon=":material/library_add:", url_path="cadastro_curso")
cadastro_disc = st.Page(telaCadastroDisciplina, title="Disciplina", icon=":material/post_add:", url_path="cadastro_disciplina")
cadastro_turma = st.Page(telaCadastroTurma, title="Turma", icon=":material/group_add:", url_path="cadastro_turma")

# Cadastros extras
cadastro_almoxarife = st.Page(telaCadastroAlmoxarife, title="Almoxarife", icon=":material/person_add:", url_path="cadastro_almoxarife")
cadastro_bolsa = st.Page(telaCadastroBolsa, title="Bolsa", icon=":material/loyalty:", url_path="cadastro_bolsa")
cadastro_campus = st.Page(telaCadastroCampus, title="Campus", icon=":material/domain_add:", url_path="cadastro_campus")
cadastro_compra = st.Page(telaCadastroCompra, title="Compra", icon=":material/add_shopping_cart:", url_path="cadastro_compra")
cadastro_financeiro = st.Page(telaCadastroFinanceiro, title="Financeiro", icon=":material/person_add:", url_path="cadastro_financeiro")
cadastro_fornecedor = st.Page(telaCadastroFornecedor, title="Fornecedor", icon=":material/person_add:", url_path="cadastro_fornecedor")
cadastro_matricula = st.Page(telaCadastroMatricula, title="Matrícula", icon=":material/assignment_add:", url_path="cadastro_matricula")
cadastro_estoque = st.Page(telaCadastroEstoque, title="Estoque", icon=":material/inventory_2:", url_path="cadastro_estoque")

from modulos.academico.pages.diario_classe_page import telaDiarioClasse
from modulos.academico.pages.designacao_cargos_page import telaDesignacaoCargos
from modulos.academico.pages.gestao_bolsas_page import telaGestaoBolsas

# Operações
operacao_diario = st.Page(telaDiarioClasse, title="Diário de Classe", icon=":material/edit_document:", url_path="diario_classe")
gestao_cargos = st.Page(telaDesignacaoCargos, title="Designação de Cargos", icon=":material/badge:", url_path="designacao_cargos")
gestao_bolsas = st.Page(telaGestaoBolsas, title="Gestão de Bolsas", icon=":material/loyalty:", url_path="gestao_bolsas")

def get_navigation():
    # Estrutura do menu lateral
    pages = {
        "Menu Principal": [
            home_page,
            cadastros_page,
        ],

        "Portal do Professor": [
            operacao_diario
        ],
        
        "Gestão Acadêmica": [
            gestao_cargos,
            gestao_bolsas
        ],

        "Cadastros": [
            cadastro_aluno,
            cadastro_prof,
            cadastro_financeiro,
            cadastro_fornecedor,
            cadastro_almoxarife,
            cadastro_campus,
            cadastro_curso,
            cadastro_disc,
            cadastro_turma,
            cadastro_bolsa,
            cadastro_compra,
            cadastro_matricula,
            cadastro_estoque
        ]
    }
    return pages