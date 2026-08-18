import streamlit as st
from modulos.pages.home_page import telaHome

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
from modulos.academico.pages.gestao_bolsas_page import telaGestaoBolsas
from modulos.academico.pages.boletim_page import telaBoletim
from modulos.academico.pages.financeiro_aluno_page import telaFinanceiroAluno

from modulos.listagem.listagem_aluno_page import telaListagemAlunos
from modulos.listagem.listagem_curso_page import telaListagemCursos
from modulos.listagem.listagem_professor_page import telaListagemProfessores
from modulos.listagem.listagem_disciplina_page import telaListagemDisciplinas
from modulos.listagem.listagem_turma_page import telaListagemTurmas
from modulos.listagem.listagem_campus_page import telaListagemCampus
from modulos.listagem.listagem_almoxarife_page import telaListagemAlmoxarifes
from modulos.listagem.listagem_financeiro_page import telaListagemFinanceiros
from modulos.listagem.listagem_bolsa_page import telaListagemBolsas
from modulos.listagem.listagem_matricula_page import telaListagemMatriculas
from modulos.listagem.listagem_compra_page import telaListagemCompras
from modulos.listagem.listagem_fornecedor_page import telaListagemFornecedores
from modulos.listagem.listagem_produto_page import telaListagemProdutos

from modulos.view.view_aluno_page import telaViewAluno
from modulos.view.view_curso_page import telaViewCurso
from modulos.view.view_professor_page import telaViewProfessor
from modulos.view.view_disciplina_page import telaViewDisciplina
from modulos.view.view_turma_page import telaViewTurma
from modulos.view.view_campus_page import telaViewCampus
from modulos.view.view_almoxarife_page import telaViewAlmoxarife
from modulos.view.view_financeiro_page import telaViewFinanceiro
from modulos.view.view_bolsa_page import telaViewBolsa
from modulos.view.view_matricula_page import telaViewMatricula
from modulos.view.view_compra_page import telaViewCompra
from modulos.view.view_fornecedor_page import telaViewFornecedor
from modulos.view.view_produto_page import telaViewProduto

from modulos.cadastros.pages.edicao.editar_aluno_page import telaEdicaoAluno
from modulos.cadastros.pages.edicao.editar_professor_page import telaEdicaoProfessor
from modulos.cadastros.pages.edicao.editar_almoxarife_page import telaEdicaoAlmoxarife
from modulos.cadastros.pages.edicao.editar_financeiro_page import telaEdicaoFinanceiro
from modulos.cadastros.pages.edicao.editar_campus_page import telaEdicaoCampus
from modulos.cadastros.pages.edicao.editar_curso_page import telaEdicaoCurso
from modulos.cadastros.pages.edicao.editar_disciplina_page import telaEdicaoDisciplina
from modulos.cadastros.pages.edicao.editar_turma_page import telaEdicaoTurma
from modulos.cadastros.pages.edicao.editar_fornecedor_page import telaEdicaoFornecedor

from modulos.dashboard.dashboard_geral_page import telaDashboardGeral
from modulos.dashboard.dashboard_academico_page import telaDashboardAcademico
from modulos.dashboard.dashboard_financeiro_page import telaDashboardFinanceiro
from modulos.dashboard.dashboard_operacional_page import telaDashboardOperacional
from modulos.estoque.movimentacao_page import telaMovimentacaoEstoque

# Páginas principais
home_page = st.Page(telaHome, title="Página Inicial", icon=":material/home:", default=True, url_path="home")

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
cadastro_estoque = st.Page(telaCadastroEstoque, title="Produto", icon=":material/inventory_2:", url_path="cadastro_estoque")

# Listagens
listagem_aluno_page = st.Page(telaListagemAlunos, title="Aluno", icon=":material/contacts:",url_path="listagem_alunos")
listagem_curso_page = st.Page(telaListagemCursos, title="Curso", icon=":material/library_books:",url_path="listagem_cursos")
listagem_professor_page = st.Page(telaListagemProfessores, title="Professor", icon=":material/groups:", url_path="listagem_professores")
listagem_disciplina_page = st.Page(telaListagemDisciplinas, title="Disciplina", icon=":material/list_alt:", url_path="listagem_disciplinas")
listagem_turma_page = st.Page(telaListagemTurmas, title="Turma", icon=":material/groups:", url_path="listagem_turmas")
listagem_campus_page = st.Page(telaListagemCampus, title="Campus", icon=":material/domain:", url_path="listagem_campus")
listagem_almoxarife_page = st.Page(telaListagemAlmoxarifes, title="Almoxarifes", icon=":material/inventory_2:", url_path="listagem_almoxarifes")
listagem_financeiro_page = st.Page(telaListagemFinanceiros, title="Financeiro", icon=":material/payments:", url_path="listagem_financeiro")
listagem_bolsa_page = st.Page(telaListagemBolsas, title="Bolsas", icon=":material/sell:", url_path="listagem_bolsas")
listagem_matricula_page = st.Page(telaListagemMatriculas, title="Matrículas", icon=":material/assignment:", url_path="listagem_matriculas")
listagem_compra_page = st.Page(telaListagemCompras, title="Compra", icon=":material/shopping_cart:", url_path="listagem_compras")
listagem_fornecedor_page = st.Page(telaListagemFornecedores, title="Fornecedor", icon=":material/local_shipping:", url_path="listagem_fornecedores")
listagem_produto_page = st.Page(telaListagemProdutos, title="Produto", icon=":material/inventory:", url_path="listagem_produtos")

#visualizações
view_aluno_page = st.Page(telaViewAluno, title="Aluno", icon=":material/person_search:", url_path="view_aluno")
view_curso_page = st.Page(telaViewCurso, title="Curso", icon=":material/auto_stories:", url_path="view_curso")
view_professor_page = st.Page(telaViewProfessor, title="Professor", icon=":material/person_search:", url_path="view_professor")
view_disciplina_page = st.Page(telaViewDisciplina, title="Disciplina", icon=":material/preview:", url_path="view_disciplina")
view_turma_page = st.Page(telaViewTurma, title="Turma", icon=":material/group_search:", url_path="view_turma")
view_campus_page = st.Page(telaViewCampus, title="Campus", icon=":material/domain_verification:", url_path="view_campus")
view_almoxarife_page = st.Page(telaViewAlmoxarife, title="Almoxarifes", icon=":material/person_search:", url_path="view_almoxarife")
view_financeiro_page = st.Page(telaViewFinanceiro, title="Financeiro", icon=":material/person_search:", url_path="view_financeiro")
view_bolsa_page = st.Page(telaViewBolsa, title="Bolsa", icon=":material/sell:", url_path="view_bolsa")
view_matricula_page = st.Page(telaViewMatricula, title="Matrículas", icon=":material/assignment_ind:", url_path="view_matricula")
view_compra_page = st.Page(telaViewCompra, title="Compra", icon=":material/receipt_long:", url_path="view_compra")
view_fornecedor_page = st.Page(telaViewFornecedor, title="Fornecedor", icon=":material/storefront:", url_path="view_fornecedor")
view_produto_page = st.Page(telaViewProduto, title="Produto", icon=":material/category:", url_path="view_produto")

# Edições (Pessoas)
editar_aluno_page = st.Page(telaEdicaoAluno, title="Aluno", icon=":material/edit:", url_path="editar_aluno")
editar_professor_page = st.Page(telaEdicaoProfessor, title="Professor", icon=":material/edit:", url_path="editar_professor")
editar_almoxarife_page = st.Page(telaEdicaoAlmoxarife, title="Almoxarife", icon=":material/edit:", url_path="editar_almoxarife")
editar_financeiro_page = st.Page(telaEdicaoFinanceiro, title="Financeiro", icon=":material/edit:", url_path="editar_financeiro")

# Edições (Outros)
editar_campus_page = st.Page(telaEdicaoCampus, title="Campus", icon=":material/edit:", url_path="editar_campus")
editar_curso_page = st.Page(telaEdicaoCurso, title="Curso", icon=":material/edit:", url_path="editar_curso")
editar_disciplina_page = st.Page(telaEdicaoDisciplina, title="Disciplina", icon=":material/edit:", url_path="editar_disciplina")
editar_turma_page = st.Page(telaEdicaoTurma, title="Turma", icon=":material/edit:", url_path="editar_turma")
editar_fornecedor_page = st.Page(telaEdicaoFornecedor, title="Fornecedor", icon=":material/edit:", url_path="editar_fornecedor")

# Dashboards
dashboard_geral_page = st.Page(telaDashboardGeral, title="Dashboard Geral", icon=":material/dashboard:")
dashboard_academico_page = st.Page(telaDashboardAcademico, title="Dashboard Acadêmico", icon=":material/school:")
dashboard_financeiro_page = st.Page(telaDashboardFinanceiro, title="Dashboard Financeiro", icon=":material/account_balance:")
dashboard_operacional_page = st.Page(telaDashboardOperacional, title="Dashboard Operacional", icon=":material/engineering:")

from modulos.academico.pages.diario_classe_page import telaDiarioClasse
from modulos.academico.pages.designacao_cargos_page import telaDesignacaoCargos
from modulos.academico.pages.gestao_bolsas_page import telaGestaoBolsas
from modulos.academico.pages.renovar_matricula_page import telaRenovarMatricula
from modulos.financeiro.pages.gestao_financeira_page import telaGestaoFinanceira

# Operações
operacao_diario = st.Page(telaDiarioClasse, title="Diário de Classe", icon=":material/edit_document:", url_path="diario_classe")
gestao_financeira = st.Page(telaGestaoFinanceira, title="Gestão Financeira", icon=":material/account_balance:", url_path="gestao_financeira")

# Gestão Acadêmica
gestao_cargos = st.Page(telaDesignacaoCargos, title="Designação de Cargos", icon=":material/badge:", url_path="designacao_cargos")
gestao_bolsas = st.Page(telaGestaoBolsas, title="Gestão de Bolsas", icon=":material/loyalty:", url_path="gestao_bolsas")

# Portal do Aluno
meu_boletim = st.Page(telaBoletim, title="Meu Boletim", icon=":material/school:", url_path="meu_boletim")
meu_financeiro = st.Page(telaFinanceiroAluno, title="Meu Financeiro", icon=":material/payments:", url_path="meu_financeiro")
renovar_matricula = st.Page(telaRenovarMatricula, title="Renovar Matrícula", icon=":material/school:", url_path="renovar_matricula")

# Movimentação
movimentacao_estoque_page = st.Page(telaMovimentacaoEstoque, title="Movimentação", icon=":material/swap_vert:", url_path="movimentacao_estoque")

def get_navigation():
    roles = st.session_state.get("roles", [])

    # Estrutura do menu lateral
    pages = {
        "Menu Principal": [
            home_page
        ]
    }

    if "ADMIN" in roles or "REITOR" in roles:
        pages["Dashboards"] = [dashboard_geral_page, dashboard_academico_page, dashboard_financeiro_page, dashboard_operacional_page]

    # Aluno
    if "ALUNO" in roles:
        pages["Portal do Aluno"] = [meu_boletim, meu_financeiro, renovar_matricula]

    # Professor
    if "PROFESSOR" in roles:
        pages["Portal do Professor"] = [operacao_diario]
    
    # Cadastros e Gestões de Alto Nível
    cadastros_list = []
    operacoes_list = []

    # Admin tem acesso a absolutamente tudo

    if "ADMIN" in roles:

        operacoes_list.append(gestao_financeira)
        
        pages["Operações"] = operacoes_list

        pages["Gestão Acadêmica"] = [gestao_cargos, gestao_bolsas]
        cadastros_list.extend([
            cadastro_aluno, cadastro_prof, cadastro_financeiro, cadastro_almoxarife,
            cadastro_campus, cadastro_curso, cadastro_disc, cadastro_turma,
            cadastro_matricula, cadastro_bolsa, cadastro_compra, cadastro_fornecedor, cadastro_estoque
        ])

    if "ADMIN" in roles:
        pages["Listagens"] = [listagem_aluno_page,
            listagem_professor_page,
            listagem_financeiro_page,
            listagem_almoxarife_page,
            listagem_campus_page,
            listagem_curso_page,
            listagem_disciplina_page,
            listagem_turma_page,
            listagem_matricula_page,
            listagem_bolsa_page,
            listagem_compra_page,
            listagem_fornecedor_page,
            listagem_produto_page
        ]
        
        pages["Visualizações"] = [view_aluno_page,
            view_professor_page,
            view_financeiro_page,
            view_almoxarife_page,
            view_campus_page,
            view_curso_page,
            view_disciplina_page,
            view_turma_page,
            view_matricula_page,
            view_bolsa_page,
            view_compra_page,
            view_fornecedor_page,
            view_produto_page
        ]
        
        pages["Edições (Oculto)"] = [
            editar_aluno_page,
            editar_professor_page,
            editar_almoxarife_page,
            editar_financeiro_page,
            editar_campus_page,
            editar_curso_page,
            editar_disciplina_page,
            editar_turma_page,
            editar_fornecedor_page
        ]

    # Reitor tem acesso executivo (C-Level)
    elif "REITOR" in roles:
        pages["Gestão Acadêmica"] = [gestao_bolsas]
        cadastros_list.extend([
            cadastro_prof,
            cadastro_curso
        ])

    # Financeiro
    if "FINANCEIRO" in roles and "ADMIN" not in roles:
        if "Dashboards" not in pages:
            pages["Dashboards"] = []
        if dashboard_financeiro_page not in pages["Dashboards"]:
            pages["Dashboards"].append(dashboard_financeiro_page)
            
        if cadastro_compra not in cadastros_list:
            cadastros_list.append(cadastro_compra)
        if cadastro_fornecedor not in cadastros_list:
            cadastros_list.append(cadastro_fornecedor)
        if gestao_financeira not in operacoes_list:
            operacoes_list.append(gestao_financeira)

    # Almoxarife
    if "ALMOXARIFE" in roles and "ADMIN" not in roles:
        if cadastro_estoque not in cadastros_list:
            cadastros_list.append(cadastro_estoque)

        if movimentacao_estoque_page not in operacoes_list:
            operacoes_list.append(movimentacao_estoque_page)

    if operacoes_list:
        pages["Operações"] = operacoes_list

    if cadastros_list:
        pages["Cadastros"] = cadastros_list

    return pages