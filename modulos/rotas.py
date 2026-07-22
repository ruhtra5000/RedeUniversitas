# IDs das Rotas
ROTA_HOME = "home"
ROTA_CADASTROS = "cadastros"
ROTA_CADASTRO_ALUNO = "cadastro_aluno"
ROTA_CADASTRO_PROFESSOR = "cadastro_professor"
ROTA_CADASTRO_CURSO = "cadastro_curso"
ROTA_CADASTRO_TURMA = "cadastro_turma"
ROTA_CADASTRO_DISCIPLINA = "cadastro_disciplina"
ROTA_ACADEMICO = "academico"
ROTA_FINANCEIRO = "financeiro"
ROTA_ALMOXARIFADO = "almoxarifado"
ROTA_RELATORIOS = "relatorios"

# Configuração da Sidebar
SIDEBAR_ITEMS = [
    {"id": ROTA_HOME, "label": "Página Inicial", "icon": ":material/home:"},
    {"id": ROTA_CADASTROS, "label": "Cadastros", "icon": ":material/folder:"},
    {"id": ROTA_ACADEMICO, "label": "Acadêmico", "icon": ":material/school:"},
    {"id": ROTA_FINANCEIRO, "label": "Financeiro", "icon": ":material/money_bag:"},
    {"id": ROTA_ALMOXARIFADO, "label": "Almoxarifado", "icon": ":material/inventory_2:"},
    {"id": ROTA_RELATORIOS, "label": "Relatórios", "icon": ":material/analytics:"},
]

# Mapeamento de Rotas
def get_rotas():
    from modulos.home import telaHome
    from modulos.cadastros.cadastros import telaCadastros
    from modulos.cadastros.aluno import telaCadastroAluno
    from modulos.cadastros.professor import telaCadastroProfessor
    from modulos.cadastros.curso import telaCadastroCurso
    from modulos.cadastros.disciplina import telaCadastroDisciplina
    from modulos.cadastros.turma import telaCadastroTurma

    return {
        ROTA_HOME: telaHome,
        ROTA_CADASTROS: telaCadastros,
        ROTA_CADASTRO_ALUNO: telaCadastroAluno,
        ROTA_CADASTRO_PROFESSOR: telaCadastroProfessor,
        ROTA_CADASTRO_CURSO: telaCadastroCurso,
        ROTA_CADASTRO_TURMA: telaCadastroTurma,
        ROTA_CADASTRO_DISCIPLINA: telaCadastroDisciplina,
        ROTA_ACADEMICO: None,  # Ainda em desenvolvimento
        ROTA_FINANCEIRO: None,  # Ainda em desenvolvimento
        ROTA_ALMOXARIFADO: None,  # Ainda em desenvolvimento
        ROTA_RELATORIOS: None,  # Ainda em desenvolvimento
    }