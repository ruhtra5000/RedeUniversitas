import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import database.entidades

db = st.secrets.database

# Conexão com o Postgres
DATABASE_URL = (
    f"postgresql+psycopg://{db.user}:{db.password}@{db.host}:{db.port}/{db.database_name}"
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