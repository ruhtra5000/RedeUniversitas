import streamlit as st
from modulos.pages.home_page import telaHome

# unified pages
from modulos.pages.aluno_page_unified import tela_aluno_unificada
from modulos.pages.professor_page_unified import tela_professor_unificada
from modulos.pages.curso_page_unified import tela_curso_unificada
from modulos.pages.disciplina_page_unified import tela_disciplina_unificada
from modulos.pages.turma_page_unified import tela_turma_unificada
from modulos.pages.almoxarife_page_unified import tela_almoxarife_unificada
from modulos.pages.bolsa_page_unified import tela_bolsa_unificada
from modulos.pages.campus_page_unified import tela_campus_unificada
from modulos.pages.compra_page_unified import tela_compra_unificada
from modulos.pages.financeiro_page_unified import tela_financeiro_unificada
from modulos.pages.fornecedor_page_unified import tela_fornecedor_unificada
from modulos.pages.matricula_page_unified import tela_matricula_unificada
from modulos.pages.estoque_page_unified import tela_estoque_unificada

# Edições (Pessoas)
from modulos.cadastros.pages.edicao.editar_aluno_page import telaEdicaoAluno
from modulos.cadastros.pages.edicao.editar_professor_page import telaEdicaoProfessor
from modulos.cadastros.pages.edicao.editar_almoxarife_page import telaEdicaoAlmoxarife
from modulos.cadastros.pages.edicao.editar_financeiro_page import telaEdicaoFinanceiro

# Edições (Outros)
from modulos.cadastros.pages.edicao.editar_campus_page import telaEdicaoCampus
from modulos.cadastros.pages.edicao.editar_curso_page import telaEdicaoCurso
from modulos.cadastros.pages.edicao.editar_disciplina_page import telaEdicaoDisciplina
from modulos.cadastros.pages.edicao.editar_turma_page import telaEdicaoTurma
from modulos.cadastros.pages.edicao.editar_fornecedor_page import telaEdicaoFornecedor

from modulos.academico.pages.diario_classe_page import telaDiarioClasse
from modulos.academico.pages.designacao_cargos_page import telaDesignacaoCargos
from modulos.academico.pages.gestao_bolsas_page import telaGestaoBolsas
from modulos.academico.pages.renovar_matricula_page import telaRenovarMatricula
from modulos.financeiro.pages.gestao_financeira_page import telaGestaoFinanceira
from modulos.academico.pages.boletim_page import telaBoletim
from modulos.academico.pages.financeiro_aluno_page import telaFinanceiroAluno

# Páginas principais
home_page = st.Page(telaHome, title="Página Inicial", icon=":material/home:", default=True, url_path="home")

# Gestão unificada
aluno_page = st.Page(tela_aluno_unificada, title="Alunos", icon="🎓", url_path="alunos")
professor_page = st.Page(tela_professor_unificada, title="Professores", icon="👩‍🏫", url_path="professores")
curso_page = st.Page(tela_curso_unificada, title="Cursos", icon="📚", url_path="cursos")
disciplina_page = st.Page(tela_disciplina_unificada, title="Disciplinas", icon="📘", url_path="disciplinas")
turma_page = st.Page(tela_turma_unificada, title="Turmas", icon="🏫", url_path="turmas")
almoxarife_page = st.Page(tela_almoxarife_unificada, title="Almoxarifes", icon="📦", url_path="almoxarifes")
bolsa_page = st.Page(tela_bolsa_unificada, title="Bolsas", icon="🎁", url_path="bolsas")
campus_page = st.Page(tela_campus_unificada, title="Campus", icon="🏛️", url_path="campus")
compra_page = st.Page(tela_compra_unificada, title="Compras", icon="🛒", url_path="compras")
financeiro_page = st.Page(tela_financeiro_unificada, title="Financeiro", icon="💰", url_path="financeiro")
fornecedor_page = st.Page(tela_fornecedor_unificada, title="Fornecedores", icon="🏭", url_path="fornecedores")
matricula_page = st.Page(tela_matricula_unificada, title="Matrículas", icon="📝", url_path="matriculas")
estoque_page = st.Page(tela_estoque_unificada, title="Estoque", icon="📦", url_path="estoque")

# Edições
editar_aluno_page = st.Page(telaEdicaoAluno, title="Aluno", icon=":material/edit:", url_path="editar_aluno")
editar_professor_page = st.Page(telaEdicaoProfessor, title="Professor", icon=":material/edit:", url_path="editar_professor")
editar_almoxarife_page = st.Page(telaEdicaoAlmoxarife, title="Almoxarife", icon=":material/edit:", url_path="editar_almoxarife")
editar_financeiro_page = st.Page(telaEdicaoFinanceiro, title="Financeiro", icon=":material/edit:", url_path="editar_financeiro")
editar_campus_page = st.Page(telaEdicaoCampus, title="Campus", icon=":material/edit:", url_path="editar_campus")
editar_curso_page = st.Page(telaEdicaoCurso, title="Curso", icon=":material/edit:", url_path="editar_curso")
editar_disciplina_page = st.Page(telaEdicaoDisciplina, title="Disciplina", icon=":material/edit:", url_path="editar_disciplina")
editar_turma_page = st.Page(telaEdicaoTurma, title="Turma", icon=":material/edit:", url_path="editar_turma")
editar_fornecedor_page = st.Page(telaEdicaoFornecedor, title="Fornecedor", icon=":material/edit:", url_path="editar_fornecedor")

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

def get_navigation():
    roles = st.session_state.get("roles", [])

    pages = {
        "Menu Principal": [home_page]
    }

    if "ALUNO" in roles:
        pages["Portal do Aluno"] = [meu_boletim, meu_financeiro, renovar_matricula]

    if "PROFESSOR" in roles:
        pages["Portal do Professor"] = [operacao_diario]
    
    gestao_cadastros = []
    operacoes_list = []

    if "ADMIN" in roles:
        pages["Gestão Acadêmica"] = [gestao_cargos, gestao_bolsas]
        
        gestao_cadastros.extend([
            aluno_page, professor_page, financeiro_page, almoxarife_page,
            campus_page, curso_page, disciplina_page, turma_page,
            matricula_page, bolsa_page, compra_page, fornecedor_page, estoque_page
        ])
        operacoes_list.append(gestao_financeira)
        
        pages["Edições (Oculto)"] = [
            editar_aluno_page, editar_professor_page, editar_almoxarife_page, editar_financeiro_page,
            editar_campus_page, editar_curso_page, editar_disciplina_page, editar_turma_page, editar_fornecedor_page
        ]

    elif "REITOR" in roles:
        pages["Gestão Acadêmica"] = [gestao_bolsas]
        gestao_cadastros.extend([professor_page, curso_page])

    if "FINANCEIRO" in roles and "ADMIN" not in roles:
        if compra_page not in gestao_cadastros:
            gestao_cadastros.append(compra_page)
        if fornecedor_page not in gestao_cadastros:
            gestao_cadastros.append(fornecedor_page)
        if gestao_financeira not in operacoes_list:
            operacoes_list.append(gestao_financeira)

    if "ALMOXARIFE" in roles and "ADMIN" not in roles:
        if estoque_page not in gestao_cadastros:
            gestao_cadastros.append(estoque_page)

    if operacoes_list:
        pages["Operações"] = operacoes_list

    if gestao_cadastros:
        pages["Gestão de Cadastros"] = gestao_cadastros

    return pages