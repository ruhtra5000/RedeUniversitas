from modulos.dashboard.dashboard_db import *


#  _____                     _ 
# |  __ \                   | |
# | |  \/  ___  _ __   __ _ | |
# | | __  / _ \| '__| / _` || |
# | |_\ \|  __/| |   | (_| || |
#  \____/ \___||_|    \__,_||_|

# Retorna a quantidade de alunos ativos (em situação regular)
def alunosAtivosTotal():
    return dbContarAlunosAtivos()

def alunosAtivosPorCampus(idCampus: int):
    return dbContarAlunosAtivos(idCampus=idCampus)

def alunosAtivosPorCurso(idCurso: int):
    return dbContarAlunosAtivos(idCurso=idCurso)

# Retorna a quantidade de alunos formados
def alunosFormadosTotal():
    return dbContarAlunosFormados()

def alunosFormadosPorCampus(idCampus: int):
    return dbContarAlunosFormados(idCampus=idCampus)

def alunosFormadosPorCurso(idCurso: int):
    return dbContarAlunosFormados(idCurso=idCurso)

# Retorna a quantidade de alunos evadidos
def alunosEvadidosTotal():
    return dbContarAlunosEvadidos()

def alunosEvadidosPorCampus(idCampus: int):
    return dbContarAlunosEvadidos(idCampus=idCampus)

def alunosEvadidosPorCurso(idCurso: int):
    return dbContarAlunosEvadidos(idCurso=idCurso)

# Retorna a quantidade de alunos trancados
def alunosTrancadosTotal():
    return dbContarAlunosTrancados()

def alunosTrancadosPorCampus(idCampus: int):
    return dbContarAlunosTrancados(idCampus=idCampus)

def alunosTrancadosPorCurso(idCurso: int):
    return dbContarAlunosTrancados(idCurso=idCurso)

# Calcula a taxa de evasão geral
def taxaEvasaoGeral(): # Saída em porcentagem
    return dbCalcularTaxaEvasao() * 100

# Retorna a quantidade de professores
def professoresTotal():
    return dbContarProfessores()

def professoresPorCampus(idCampus: int):
    return dbContarProfessores(idCampus=idCampus)

def professoresPorCurso(idCurso: int):
    return dbContarProfessores(idCurso=idCurso)

# Retorna a quantidade de cursos
def cursosTotal():
    return dbContarCursos()

def cursosPorCampus(idCampus: int):
    return dbContarCursos(idCampus)


#   ___                    _                   _              
#  / _ \                  | |                 (_)             
# / /_\ \  ___   __ _   __| |  ___  _ __ ___   _   ___   ___  
# |  _  | / __| / _` | / _` | / _ \| '_ ` _ \ | | / __| / _ \ 
# | | | || (__ | (_| || (_| ||  __/| | | | | || || (__ | (_) |
# \_| |_/ \___| \__,_| \__,_| \___||_| |_| |_||_| \___| \___/ 

# Calcula o coeficiente de rendimento médio
def crMedioTotal():
    return dbCalcularCoefRendMedio()

def crMedioPorCampus(idCampus: int):
    return dbCalcularCoefRendMedio(idCampus=idCampus)

def crMedioCurso(idCurso: int):
    return dbCalcularCoefRendMedio(idCurso=idCurso)

# Retorna a quantidade de alunos em categorias de desempenho 
# (Excelente, Bom, Regular e Ruim)
def agruparAlunosDesempenhoGeral():
    return dbAgruparAlunosDesempenho()

def agruparAlunosDesempenhoPorCampus(idCampus: int):
    return dbAgruparAlunosDesempenho(idCampus=idCampus)

def agruparAlunosDesempenhoPorCurso(idCurso: int):
    return dbAgruparAlunosDesempenho(idCurso=idCurso)

# Retorna dados dos alunos com baixo desempenho academico
# (Baixo desempenho: CR < 5.5 ou 3+ reprovaçoes)
def listarAlunosBaixoDesempenhoGeral():
    return dbAlunosBaixoDesempenho()

def listarAlunosBaixoDesempenhoPorCampus(idCampus: int):
    return dbAlunosBaixoDesempenho(idCampus=idCampus)

def listarAlunosBaixoDesempenhoPorCurso(idCurso: int):
    return dbAlunosBaixoDesempenho(idCurso=idCurso)


# ______  _                                   _              
# |  ___|(_)                                 (_)             
# | |_    _  _ __    __ _  _ __    ___   ___  _  _ __   ___  
# |  _|  | || '_ \  / _` || '_ \  / __| / _ \| || '__| / _ \ 
# | |    | || | | || (_| || | | || (__ |  __/| || |   | (_) |
# \_|    |_||_| |_| \__,_||_| |_| \___| \___||_||_|    \___/ 

# Calcula o valor recebido total
def calcularReceitaTotal():
    return dbCalcularReceita()

def calcularReceitaPorCampus(idCampus: int):
    return dbCalcularReceita(idCampus=idCampus)

def calcularReceitaPorCurso(idCurso: int):
    return dbCalcularReceita(idCurso=idCurso)

# Calcula o valor a receber total
def cacularTotalAReceberGeral():
    return dbCalcularTotalAReceber()

def cacularTotalAReceberPorCampus(idCampus: int):
    return dbCalcularTotalAReceber(idCampus=idCampus)

def cacularTotalAReceberPorCurso(idCurso: int):
    return dbCalcularTotalAReceber(idCurso=idCurso)

# Retorna a quantidade de alunos inadimplentes
def alunosInadimplentesTotal():
    return dbContarAlunosInadimplentes()

def alunosInadimplentesPorCampus(idCampus: int):
    return dbContarAlunosInadimplentes(idCampus=idCampus)

def alunosInadimplentesPorCurso(idCurso: int):
    return dbContarAlunosInadimplentes(idCurso=idCurso)

# Calcula a taxa de inadimplencia (saída em porcentagem)
def taxaInadimplenciaGeral():
    return dbCalcularTaxaInadimplencia() * 100

def taxaInadimplenciaPorCampus(idCampus: int):
    return dbCalcularTaxaInadimplencia(idCampus=idCampus) * 100

def taxaInadimplenciaPorCurso(idCurso: int):
    return dbCalcularTaxaInadimplencia(idCurso=idCurso) * 100

# Calcula o valor monetário não pago por inadimplencia
def valorTotalInadimplente():
    return dbCalcularValorTotalInadimplente()

def valorTotalInadimplentePorCampus(idCampus: int):
    return dbCalcularValorTotalInadimplente(idCampus=idCampus)

def valorTotalInadimplentePorCurso(idCurso: int):
    return dbCalcularValorTotalInadimplente(idCurso=idCurso)

# Retorna a quantidade de mensalidades vencidas
def mensalidadesVencidasTotal():
    return dbContarMensalidadesVencidas()

def mensalidadesVencidasPorCampus(idCampus: int):
    return dbContarMensalidadesVencidas(idCampus=idCampus)

def mensalidadesVencidasPorCurso(idCurso: int):
    return dbContarMensalidadesVencidas(idCurso=idCurso)

# Calcula a divida média (inadimplente) por aluno
def dividaMediaTotal():
    return dbCalcularDividaMedia()

def dividaMediaPorCampus(idCampus: int):
    return dbCalcularDividaMedia(idCampus=idCampus)

def dividaMediaPorCurso(idCurso: int):
    return dbCalcularDividaMedia(idCurso=idCurso)

# Retorna a quantidade de alunos com bolsa ativa
def alunosBolsistasTotal():
    return dbContarBolsistas()

def alunosBolsistasPorCampus(idCampus: int):
    return dbContarBolsistas(idCampus=idCampus)

def alunosBolsistasPorCurso(idCurso: int):
    return dbContarBolsistas(idCurso=idCurso)

# Calcula o percentual de bolsistas com bolsa ativa em relação aos alunos ativos
def taxaBolsistaGeral():
    return dbCalcularTaxaBolsistas()

def taxaBolsistaPorCampus(idCampus: int):
    return dbCalcularTaxaBolsistas(idCampus=idCampus)

def taxaBolsistaPorCurso(idCurso: int):
    return dbCalcularTaxaBolsistas(idCurso=idCurso)

# Calcula o valor monetário total "perdido" por causa de bolsas
def valorConcedidoPorBolsaTotal():
    return dbCalcularValorConcedidoPorBolsas()

def valorConcedidoPorBolsaPorCampus(idCampus: int):
    return dbCalcularValorConcedidoPorBolsas(idCampus=idCampus)

def valorConcedidoPorBolsaPorCurso(idCurso: int):
    return dbCalcularValorConcedidoPorBolsas(idCurso=idCurso)


#  _____                                  _                       _ 
# |  _  |                                (_)                     | |
# | | | | _ __    ___  _ __   __ _   ___  _   ___   _ __    __ _ | |
# | | | || '_ \  / _ \| '__| / _` | / __|| | / _ \ | '_ \  / _` || |
# \ \_/ /| |_) ||  __/| |   | (_| || (__ | || (_) || | | || (_| || |
#  \___/ | .__/  \___||_|    \__,_| \___||_| \___/ |_| |_| \__,_||_|
#        | |                                                        
#        |_|                                                        

