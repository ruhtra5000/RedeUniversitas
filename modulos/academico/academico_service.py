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
    

# ______                __                                         
# | ___ \              / _|                                        
# | |_/ / _ __   ___  | |_   ___  ___  ___   ___   _ __   ___  ___ 
# |  __/ | '__| / _ \ |  _| / _ \/ __|/ __| / _ \ | '__| / _ \/ __|
# | |    | |   | (_) || |  |  __/\__ \\__ \| (_) || |   |  __/\__ \
# \_|    |_|    \___/ |_|   \___||___/|___/ \___/ |_|    \___||___/

def listarProfessores():
    return dbListarProfessores()
    
def listarProfessorId(idProfessor: int):
    professor = dbListarProfessorId(idProfessor)

    if professor == None:
        raise Exception(f"Professor com id {idProfessor} não existente.")
    
    return professor
    
def listarProfessorNome(nomeProfessor: str):
    return dbListarProfessorNome(nomeProfessor)
    
def listarProfessorCpf(cpfProfessor: str):
    return dbListarProfessorCpf(cpfProfessor)