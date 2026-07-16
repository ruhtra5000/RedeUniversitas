from datetime import date

from database.entidades.enums.ModalidadeCurso import ModalidadeCurso
from modulos.academico.academico_db import *
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone

#  _____                                      
# /  __ \                                     
# | /  \/  __ _  _ __ ___   _ __   _   _  ___ 
# | |     / _` || '_ ` _ \ | '_ \ | | | |/ __|
# | \__/\| (_| || | | | | || |_) || |_| |\__ \
#  \____/ \__,_||_| |_| |_|| .__/  \__,_||___/
#                          | |                
#                          |_|                

def listarCampus():
    return dbListarCampus()

def listarCampusId(idCampus: int):
    campus = dbListarCampusId(idCampus)

    if campus == None:
        raise Exception(f"Campus com id {idCampus} não existente.")
    
    return campus

def listarCampusNome(nomeCampus: str):
    return dbListarCampusNome(nomeCampus)

def editarCampus(idCampus: int, nome: str, email: str, telefone: str):
    if nome == "" or nome == None:
        raise Exception("O campo 'nome' é obrigatório.")
    
    if email != "" and not validarEmail(email):
        raise Exception("O e-mail informado não é válido.")
    
    if telefone != "" and not validarTelefone(telefone):
        raise Exception("O telefone informado não é válido.")
    
    campus = Campus(
        nome=nome,
        email=email,
        telefone=telefone
    )

    dbEditarCampus(idCampus, campus)

def definirReitor(idCampus: int, idReitor: int):
    professor = dbListarProfessorId(idReitor)

    if professor == None:
        raise Exception("O professor informado não existe.")
    if professor.campus_id != idCampus:
        raise Exception("O professor definido como reitor deve estar vinculado ao campus.")

    dbDefinirReitor(idCampus, idReitor)

def removerReitor(idCampus: int):
    dbRemoverReitor(idCampus)


#  _____                               
# /  __ \                              
# | /  \/ _   _  _ __  ___   ___   ___ 
# | |    | | | || '__|/ __| / _ \ / __|
# | \__/\| |_| || |   \__ \| (_) |\__ \
#  \____/ \__,_||_|   |___/ \___/ |___/

def listarCursos():
    return dbListarCursos()

def listarCursoId(idCurso: int):
    curso = dbListarCursoId(idCurso)

    if curso == None:
        raise Exception(f"Curso com id {idCurso} não existente.")
    
    return curso
    
def editarCurso(idCurso: int, nome: str, modalidade: ModalidadeCurso, carga_horaria: int,
                dur_min_semestre: int, dur_max_semestre: int):
    
    if nome == "" or nome == None:
        raise Exception("O campo 'nome' é obrigatório.")
    
    if carga_horaria <= 0:
        raise Exception("O valor da carga horária deve ser maior que 0.")
    
    if dur_min_semestre > dur_max_semestre:
        raise Exception("A duração mínima de semestres não pode ser maior do que a duração máxima.")

    curso = Curso(
        nome=nome,
        modalidade=modalidade,
        carga_horaria=carga_horaria,
        dur_min_semestre=dur_min_semestre,
        dur_max_semestre=dur_max_semestre
    )

    dbEditarCurso(idCurso, curso)
    
        
def definirCoordenador(idCurso: int, idCoordenador: int):
    try:
        curso = listarCursoId(idCurso)
        professor = dbListarProfessorId(idCoordenador)

        if professor == None:
            raise Exception(f"Professor com id {idCoordenador} não existente.")
        
        if professor.campus_id != curso.campus_id:
            raise Exception("O coordenador do curso deve estar vinculado ao mesmo campus do curso em questão.")
        
        dbDefinirCoordenador(idCurso, idCoordenador)

    except Exception:
        raise 

def removerCoordenador(idCurso: int):
    dbRemoverCoordenador(idCurso)


# ______  _             _         _  _                    
# |  _  \(_)           (_)       | |(_)                   
# | | | | _  ___   ___  _  _ __  | | _  _ __    __ _  ___ 
# | | | || |/ __| / __|| || '_ \ | || || '_ \  / _` |/ __|
# | |/ / | |\__ \| (__ | || |_) || || || | | || (_| |\__ \
# |___/  |_||___/ \___||_|| .__/ |_||_||_| |_| \__,_||___/
#                         | |                             
#                         |_|                             

def listarDisciplinas(idCurso: int):
    return dbListarDisciplinas(idCurso)

def listarDisciplinaId(idDisciplina: int):
    disciplina = dbListarDisciplinaId(idDisciplina)

    if disciplina == None:
        raise Exception(f"Disciplina com id {idDisciplina} não existente.")
    
    return disciplina
    
def editarDisciplina(idDisciplina: int, nome: str, carga_horaria: int, obrigatoria: bool):
    if nome == "" or nome == None:
        raise Exception("O campo 'nome' é obrigatório.")
    
    if carga_horaria <= 0:
        raise Exception("O valor da carga horária deve ser maior que 0.")
    
    disciplina = Disciplina(
        nome=nome,
        carga_horaria=carga_horaria,
        obrigatoria=obrigatoria
    )

    dbEditarDisciplina(idDisciplina, disciplina)
    
def adicionarPreRequisito(idDisciplina: int, idPreRequisito: int):
    preRequisito = PreRequisito(
        disciplina_id=idDisciplina,
        prerequisito_id=idPreRequisito
    )
    dbAdicionarPreRequisito(preRequisito)
    
def removerPreRequisito(idDisciplina: int, idPreRequisito: int):
    preRequisito = PreRequisito(
        disciplina_id=idDisciplina,
        prerequisito_id=idPreRequisito
    )
    dbRemoverPreRequisito(preRequisito)


#  _____                                
# |_   _|                               
#   | |   _   _  _ __  _ __ ___    __ _ 
#   | |  | | | || '__|| '_ ` _ \  / _` |
#   | |  | |_| || |   | | | | | || (_| |
#   \_/   \__,_||_|   |_| |_| |_| \__,_|

def listarTurmasProfessor(idProfessor: int, semestre: str):
    return dbListarTurmasProfessor(idProfessor, semestre)
    
def listarTurmasCurso(idCurso: int, semestre: str):
    return dbListarTurmasCurso(idCurso, semestre)
    
def listarTurmaId(idTurma: int):
    turma = dbListarTurmaId(idTurma)

    if turma == None:
        raise Exception(f"Turma com id {idTurma} não existente.")
    
    return turma

def alterarProfessorTurma(idTurma: int, idNovoProfessor: int):
    turma = dbListarTurmaId(idTurma)
    professor = dbListarProfessorId(idNovoProfessor)

    if turma == None:
        raise Exception(f"Turma com id {idTurma} não existente.")
    
    if professor == None:
        raise Exception(f"Professor com id {idNovoProfessor} não existente.")

    if turma.curso.campus_id != professor.campus_id:
        raise Exception(f"O novo professor designado para esta Turma deve pertencer ao Campus {turma.curso.campus.nome}.")
    
    dbAlterarProfessorTurma(idTurma, idNovoProfessor)

# Calcula a freq. relativa, atualiza coef. de rendimento e media geral e aprovacao de cada aluno
def fecharTurma(idTurma: int):
    turma = dbListarTurmaId(idTurma)

    if turma == None:
        raise Exception(f"Turma com id {idTurma} não existente.")
    else:
        for matr in turma.matriculas:
            calcularFrequenciaRelativa(matr.aluno_id, idTurma)
            atualizarCoefRendMediaGeral(matr.aluno_id)

            # Se a aprovação não foi definida até aqui,
            # significa que o aluno não atingiu a média mínima
            # ou falou a todas as provas
            if matr.aprovacao == None:
                dbDefinirAprovacao(matr.aluno_id, idTurma, False)


# ___  ___        _          _               _             
# |  \/  |       | |        (_)             | |            
# | .  . |  __ _ | |_  _ __  _   ___  _   _ | |  __ _  ___ 
# | |\/| | / _` || __|| '__|| | / __|| | | || | / _` |/ __|
# | |  | || (_| || |_ | |   | || (__ | |_| || || (_| |\__ \
# \_|  |_/ \__,_| \__||_|   |_| \___| \__,_||_| \__,_||___/

def listarMatriculaId(idAluno: int, idTurma: int):
    matricula = dbListarMatriculaId(idAluno, idTurma)

    if matricula == None:
        raise Exception(f"Matrícula de aluno com id {idAluno} e turma com id {idTurma} não existente.")
    
    return matricula
        
def lancarNota1(idAluno: int, idTurma: int, nota: Decimal):
    dbLancarNota1(idAluno, idTurma, nota)
        
def lancarNota2(idAluno: int, idTurma: int, nota: Decimal):
    dbLancarNota2(idAluno, idTurma, nota)
        
def lancarNota3(idAluno: int, idTurma: int, nota: Decimal):
    dbLancarNota3(idAluno, idTurma, nota)
        
def lancarNotaFinal(idAluno: int, idTurma: int, nota: Decimal):
    dbLancarNotaFinal(idAluno, idTurma, nota)

def cadastrarPresenca(idAluno: int, idTurma: int, qtdeAulas: int):
    dbCadastrarPresenca(idAluno, idTurma, qtdeAulas)
        
def calcularFrequenciaRelativa(idAluno: int, idTurma: int):
    matricula = listarMatriculaId(idAluno, idTurma)

    # Considerando aulas de 45 MINUTOS CADA
    aulasTotais: float = matricula.disciplina.carga_horaria * 0.75 

    freqRelativa: float = matricula.frequencia_abs / aulasTotais

    dbCalcularFrequenciaRelativa(idAluno, idTurma, freqRelativa)

    if freqRelativa < 0.75: # Freq. Minima: 75%
        dbDefinirAprovacao(idAluno, idTurma, False)
    

# ______                __                                         
# | ___ \              / _|                                        
# | |_/ / _ __   ___  | |_   ___  ___  ___   ___   _ __   ___  ___ 
# |  __/ | '__| / _ \ |  _| / _ \/ __|/ __| / _ \ | '__| / _ \/ __|
# | |    | |   | (_) || |  |  __/\__ \\__ \| (_) || |   |  __/\__ \
# \_|    |_|    \___/ |_|   \___||___/|___/ \___/ |_|    \___||___/

def listarProfessores():
    return dbListarProfessores()

def listarProfessoresCampus(idCampus: int):
    return dbListarProfessoresCampus(idCampus)
    
def listarProfessorId(idProfessor: int):
    professor = dbListarProfessorId(idProfessor)

    if professor == None:
        raise Exception(f"Professor com id {idProfessor} não existente.")
    
    return professor
    
def listarProfessorNome(nomeProfessor: str):
    return dbListarProfessorNome(nomeProfessor)
    
def listarProfessorCpf(cpfProfessor: str):
    return dbListarProfessorCpf(cpfProfessor)


#   ___   _                      
#  / _ \ | |                     
# / /_\ \| | _   _  _ __    ___  
# |  _  || || | | || '_ \  / _ \ 
# | | | || || |_| || | | || (_) |
# \_| |_/|_| \__,_||_| |_| \___/ 

def listarAlunos():
    return dbListarAlunos()

def listarAlunosCampus(idCampus: int):
    return dbListarAlunosCampus(idCampus)
    
def listarAlunosCurso(idCurso: int):
    return dbListarAlunosCurso(idCurso)
    
def listarAlunoId(idAluno: int):
    aluno = dbListarAlunoId(idAluno)

    if aluno == None:
        raise Exception(f"Aluno com id {idAluno} não existente.")
    
    return aluno
    
def atualizarCoefRendMediaGeral(idAluno: int):
    aluno = listarAlunoId(idAluno)

    mediaSoma: float = 0
    coefSoma: float = 0
    chSoma: int = 0

    for matr in aluno.matriculas:
        mediaSoma += matr.media.__float__()

        coefSoma += (matr.media.__float__() * matr.disciplina.carga_horaria)

        chSoma += matr.disciplina.carga_horaria

    media = mediaSoma / len(aluno.matriculas)
    coefRend = coefSoma / chSoma

    dbAtualizarCoefRendMediaGeral(idAluno, coefRend, media)


# ______         _                  
# | ___ \       | |                 
# | |_/ /  ___  | | ___   __ _  ___ 
# | ___ \ / _ \ | |/ __| / _` |/ __|
# | |_/ /| (_) || |\__ \| (_| |\__ \
# \____/  \___/ |_||___/ \__,_||___/

def listarBolsasCampus(idCampus: int):
    alunos = listarAlunosCampus(idCampus)

    bolsas: list[Bolsa] = []
    for aluno in alunos:
        for bolsa in aluno.bolsas:
            bolsas.append(bolsa)

    return bolsas

def listarBolsasCurso(idCurso: int):
    alunos = listarAlunosCurso(idCurso)

    bolsas: list[Bolsa] = []
    for aluno in alunos:
        for bolsa in aluno.bolsas:
            bolsas.append(bolsa)

    return bolsas

def listarBolsasAluno(idAluno: int):
    return dbListarBolsasAluno(idAluno)

def listarBolsasAtivas():
    return dbListarBolsasAtivas()

def listarBolsasAtivasAluno(idAluno: int):
    return dbListarBolsasAtivasAluno(idAluno)

def listarBolsaId(idBolsa: int):
    bolsa = dbListarBolsaId(idBolsa)

    if bolsa == None:
        raise Exception(f"Bolsa com id {idBolsa} não existente.")
    
    return bolsa

def editarBolsa(idBolsa: int, tipo_bolsa: str, percentual_desconto: float, data_fim: date, status: StatusBolsa):
    bolsa = listarBolsaId(idBolsa)

    if status == StatusBolsa.ATIVA:
        bolsasAluno: list[Bolsa] = listarBolsasAtivasAluno(bolsa.aluno_id)
        
        if bolsasAluno.count(bolsa) > 0:
            bolsasAluno.remove(bolsa)

        if bolsasAluno != []:
            raise Exception(f"O aluno em questão já tem uma bolsa ativa vinculada a si.")
    
    if data_fim < bolsa.data_inicio:
        raise Exception(f"A data de início deve vir antes da data de fim.")

    novaBolsa = Bolsa(
        tipo_bolsa = tipo_bolsa,
        percentual_desconto = percentual_desconto,
        data_fim = data_fim,
        status = status
    )

    dbEditarBolsa(idBolsa, novaBolsa)


# ___  ___                          _  _      _             _            
# |  \/  |                         | |(_)    | |           | |           
# | .  . |  ___  _ __   ___   __ _ | | _   __| |  __ _   __| |  ___  ___ 
# | |\/| | / _ \| '_ \ / __| / _` || || | / _` | / _` | / _` | / _ \/ __|
# | |  | ||  __/| | | |\__ \| (_| || || || (_| || (_| || (_| ||  __/\__ \
# \_|  |_/ \___||_| |_||___/ \__,_||_||_| \__,_| \__,_| \__,_| \___||___/

def listarMensalidades():
    return dbListarMensalidades()

def listarMensalidadesCampus(idCampus: int):
    return dbListarMensalidadesCampus(idCampus)

def listarMensalidadesCurso(idCurso: int):
    return dbListarMensalidadesCurso(idCurso)

def listarMensalidadesAluno(idAluno: int):
    return dbListarMensalidadesAluno(idAluno)
    
def listarMensalidadeId(idMensalidade: int):
    mensalidade = dbListarMensalidadeId(idMensalidade)

    if mensalidade == None:
        raise Exception(f"Mensalidade com id {idMensalidade} não existente.")
    
    return mensalidade
