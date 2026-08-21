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

def taxaEvasaoPorCampus(idCampus: int):
    return dbCalcularTaxaEvasao(idCampus=idCampus) * 100

def taxaEvasaoPorCurso(idCurso: int):
    return dbCalcularTaxaEvasao(idCurso=idCurso) * 100

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
def calcularReceitaTotal(
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularReceita(dataIni=dataIni, dataFim=dataFim)

def calcularReceitaPorCampus(
        idCampus: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularReceita(idCampus=idCampus, dataIni=dataIni, dataFim=dataFim)

def calcularReceitaPorCurso(
        idCurso: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularReceita(idCurso=idCurso, dataIni=dataIni, dataFim=dataFim)

# Calcula o valor a receber total
def cacularTotalAReceberGeral(
        dataIni: date | None = None,
        dataFim: date | None = None    
    ):
    return dbCalcularTotalAReceber(dataIni=dataIni, dataFim=dataFim)

def cacularTotalAReceberPorCampus(
        idCampus: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularTotalAReceber(idCampus=idCampus, dataIni=dataIni, dataFim=dataFim)

def cacularTotalAReceberPorCurso(
        idCurso: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularTotalAReceber(idCurso=idCurso, dataIni=dataIni, dataFim=dataFim)

# Retorna a quantidade de alunos inadimplentes
def alunosInadimplentesTotal(
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbContarAlunosInadimplentes(dataIni=dataIni, dataFim=dataFim)

def alunosInadimplentesPorCampus(
        idCampus: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbContarAlunosInadimplentes(idCampus=idCampus, dataIni=dataIni, dataFim=dataFim)

def alunosInadimplentesPorCurso(
        idCurso: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbContarAlunosInadimplentes(idCurso=idCurso, dataIni=dataIni, dataFim=dataFim)

# Calcula a taxa de inadimplencia (saída em porcentagem)
def taxaInadimplenciaGeral(
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularTaxaInadimplencia(dataIni=dataIni, dataFim=dataFim) * 100

def taxaInadimplenciaPorCampus(
        idCampus: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularTaxaInadimplencia(idCampus=idCampus, dataIni=dataIni, dataFim=dataFim) * 100

def taxaInadimplenciaPorCurso(
        idCurso: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularTaxaInadimplencia(idCurso=idCurso, dataIni=dataIni, dataFim=dataFim) * 100

# Calcula o valor monetário não pago por inadimplencia
def valorTotalInadimplente(
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularValorTotalInadimplente(dataIni=dataIni, dataFim=dataFim)

def valorTotalInadimplentePorCampus(
        idCampus: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularValorTotalInadimplente(idCampus=idCampus, dataIni=dataIni, dataFim=dataFim)

def valorTotalInadimplentePorCurso(
        idCurso: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularValorTotalInadimplente(idCurso=idCurso, dataIni=dataIni, dataFim=dataFim)

# Retorna a quantidade de mensalidades vencidas
def mensalidadesVencidasTotal(
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbContarMensalidadesVencidas(dataIni=dataIni, dataFim=dataFim)

def mensalidadesVencidasPorCampus(
        idCampus: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbContarMensalidadesVencidas(idCampus=idCampus, dataIni=dataIni, dataFim=dataFim)

def mensalidadesVencidasPorCurso(
        idCurso: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbContarMensalidadesVencidas(idCurso=idCurso, dataIni=dataIni, dataFim=dataFim)

# Calcula a divida média (inadimplente) por aluno
def dividaMediaTotal(
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularDividaMedia(dataIni=dataIni, dataFim=dataFim)

def dividaMediaPorCampus(
        idCampus: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularDividaMedia(idCampus=idCampus, dataIni=dataIni, dataFim=dataFim)

def dividaMediaPorCurso(
        idCurso: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularDividaMedia(idCurso=idCurso, dataIni=dataIni, dataFim=dataFim)

# Retorna a quantidade de alunos com bolsa ativa
def alunosBolsistasTotal(
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbContarBolsistas(dataIni=dataIni, dataFim=dataFim)

def alunosBolsistasPorCampus(
        idCampus: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbContarBolsistas(idCampus=idCampus, dataIni=dataIni, dataFim=dataFim)

def alunosBolsistasPorCurso(
        idCurso: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbContarBolsistas(idCurso=idCurso, dataIni=dataIni, dataFim=dataFim)

# Calcula o percentual de bolsistas com bolsa ativa em relação aos alunos ativos
def taxaBolsistaGeral(
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularTaxaBolsistas(dataIni=dataIni, dataFim=dataFim)

def taxaBolsistaPorCampus(
        idCampus: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularTaxaBolsistas(idCampus=idCampus, dataIni=dataIni, dataFim=dataFim)

def taxaBolsistaPorCurso(
        idCurso: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularTaxaBolsistas(idCurso=idCurso, dataIni=dataIni, dataFim=dataFim)

# Calcula o valor monetário total "perdido" por causa de bolsas
def valorConcedidoPorBolsaTotal(
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularValorConcedidoPorBolsas(dataIni=dataIni, dataFim=dataFim)

def valorConcedidoPorBolsaPorCampus(
        idCampus: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularValorConcedidoPorBolsas(idCampus=idCampus, dataIni=dataIni, dataFim=dataFim)

def valorConcedidoPorBolsaPorCurso(
        idCurso: int,
        dataIni: date | None = None,
        dataFim: date | None = None
    ):
    return dbCalcularValorConcedidoPorBolsas(idCurso=idCurso, dataIni=dataIni, dataFim=dataFim)


#  _____                                  _                       _ 
# |  _  |                                (_)                     | |
# | | | | _ __    ___  _ __   __ _   ___  _   ___   _ __    __ _ | |
# | | | || '_ \  / _ \| '__| / _` | / __|| | / _ \ | '_ \  / _` || |
# \ \_/ /| |_) ||  __/| |   | (_| || (__ | || (_) || | | || (_| || |
#  \___/ | .__/  \___||_|    \__,_| \___||_| \___/ |_| |_| \__,_||_|
#        | |                                                        
#        |_|                                                        

# Retorna a quantidade de produtos com mesmo nome (independe de marca), mais ou menos o "tipo"
def tipoProdutosGeral():
    return dbContarTipoProduto()

def tipoProdutosPorCampus(idCampus: int):
    return dbContarTipoProduto(idCampus=idCampus)

# Retorna a quantidade de produtos em estoque
def qtdeProdutosGeral():
    return dbContarQtdeProdutos()

def qtdeProdutosPorCampus(idCampus: int):
    return dbContarQtdeProdutos(idCampus=idCampus)

# Retorna a quantidade de produtos com estoque menor que o mínimo
def qtdeProdutosBaixoEstoqueGeral():
    return dbContarProdutosComEstoqueBaixo()

def qtdeProdutosBaixoEstoquePorCampus(idCampus: int):
    return dbContarProdutosComEstoqueBaixo(idCampus=idCampus)

# Lista os produtos com estoque menor que o mínimo
def listarProdutosBaixoEstoqueGeral():
    return dbListarProdutosComEstoqueBaixo()

def listarProdutosBaixoEstoquePorCampus(idCampus: int):
    return dbListarProdutosComEstoqueBaixo(idCampus=idCampus)

# Retorna a quantidade de produtos sem estoque
def qtdeProdutosSemEstoqueGeral():
    return dbContarProdutosSemEstoque()

def qtdeProdutosSemEstoquePorCampus(idCampus: int):
    return dbContarProdutosSemEstoque(idCampus=idCampus)

# Lista os produtos sem estoque
def listarProdutosSemEstoqueGeral():
    return dbListarProdutosSemEstoque()

def listarProdutosSemEstoquePorCampus(idCampus: int):
    return dbListarProdutosSemEstoque(idCampus=idCampus)

# Lista nome, marca e quantidade de movimentações de SAIDA dos 5 produtos mais usados
def produtosMaisUsadosGeral():
    return dbCalcularProdutosMaisUsados()

def produtosMaisUsadosPorCampus(idCampus: int):
    return dbCalcularProdutosMaisUsados(idCampus=idCampus)

# Lista a quantidade de movimentações em si e a quantidade de unidades 
# movimentadas por tipo de movimentação (entrada, saida, ajuste e perda)
def movimentacoesPorTipoGeral():
    return dbContarQtdeEUnidadeMovimentacoes()

def movimentacoesPorTipoPorCampus(idCampus: int):
    return dbContarQtdeEUnidadeMovimentacoes(idCampus=idCampus)

# Retorna a quantidade de movimentações dos últimos 6 meses
# agrupadas por tipo de movimentação e mês
def movimentacoesRecentesGeral():
    return dbMovimentacoesUltimosMeses()

def movimentacoesRecentesPorCampus(idCampus: int):
    return dbMovimentacoesUltimosMeses(idCampus=idCampus)

# Retorna a quantidade de compras realizadas
def qtdeComprasGeral():
    return dbContarCompras()

def qtdeComprasPorCampus(idCampus: int):
    return dbContarCompras(idCampus=idCampus)

# Retorna o valor total gasto em compras
def valorTotalCompradoGeral():
    return dbCalcularValorTotalComprado()

def valorTotalCompradoPorCampus(idCampus: int):
    return dbCalcularValorTotalComprado(idCampus=idCampus)

# Retorna o valor médio de uma compra
def valorMedioCompraGeral():
    return dbCalcularTicketMedio()

def valorMedioCompraPorCampus(idCampus: int):
    return dbCalcularTicketMedio(idCampus=idCampus)

# Lista nome, marca, unidades compradas, e valor gasto dos 5 produtos mais
# vendidos por unidade, agrupados por produto
def produtosMaisCompradosGeral():
    return dbListarProdutosMaisComprados()

def produtosMaisCompradosPorCampus(idCampus: int):
    return dbListarProdutosMaisComprados(idCampus=idCampus)

# Retorna a quantidade de fornecedores
def qtdeFornecedores():
    return dbContarFornecedores()

# Lista os dados dos fornecedores, quantidade de vendas, valor gasto por fornecedor
# dos 5 fornecedores mais usados por qtde de vendas, agrupados por fornecedor
def fornecedoresMaisUsadosGeral():
    return dbFornecedoresMaisUsados()

def fornecedoresMaisUsadosPorCampus(idCampus: int):
    return dbFornecedoresMaisUsados(idCampus=idCampus)
