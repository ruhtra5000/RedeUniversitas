from decimal import Decimal

from sqlalchemy.exc import SQLAlchemyError
from validate_docbr.CNPJ import CNPJ

from database.Conexao import SessionLocal
from database.entidades.Caixa import Caixa
from database.entidades.Campus import Campus
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
import database.entidades





# Aqui seria a "camada de serviço", onde voce pode pegar 
# os dados da interface e/ou fazer alguma validação de regra de negocio 
def criarCampus(campus: Campus, valorInicialCaixa: int = 0):
    try:
        if not CNPJ().validate(campus.cnpj):
            raise Exception("O CNPJ disponibilizado não é válido.")
        
        if campus.email != "":
            if not validarEmail(campus.email):
                raise Exception("O E-mail disponibilizado não é válido.")
            
        if campus.telefone != "":
            if not validarTelefone(campus.telefone):
                raise Exception("O telefone disponibilizado não é válido.")

        # Criar Caixa vinculado a esse Campus
        caixa = Caixa(
            valor_caixa = Decimal(valorInicialCaixa)
        )

        dbCriarCampus(campus, caixa)

    except SQLAlchemyError:
        raise


# Aqui seria a camada de dados (somente ela deve interagir diretamente com o banco)
def dbCriarCampus(campus: Campus, caixa: Caixa):
    with SessionLocal() as session:
        try:
            # Criação do Campus
            session.add(campus)
            session.commit()
            
            # Pegando o id atribuido
            session.refresh(campus)
            caixa.campus_id = campus.id

            # Criando o Caixa
            session.add(caixa)
            session.commit()
        
        except SQLAlchemyError:
            session.rollback()
            raise