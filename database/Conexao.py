from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Conexão com o Postgres
DATABASE_URL = (
    "postgresql+psycopg://user_universitas:universitas123@localhost:5432/rede_universitas"
)

# Criação da engine
engine = create_engine(
    DATABASE_URL,
    echo=True
)

# Habilitar criação de sessões
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)