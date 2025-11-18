from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from mangum import Mangum
import logging

# ------------------------------------------------------------
# Lambda FastAPI conectando em Postgres
# Observação: NÃO roda Flyway aqui; o banco já deve estar migrado
# via pipeline (GitHub Actions). A Lambda apenas consome o banco.
# ------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lê variáveis de ambiente fornecidas pelo Terraform na Lambda
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Engine/Session do SQLAlchemy (conexão com Postgres)
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

app = FastAPI(title="Catalogo API (Flyway)", version="1.0.0")

@app.on_event("startup")
def on_startup():
    logger.info("🚀 API iniciando (sem migrations na Lambda)...")

# Dependência de sessão para endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CORS básico (ajuste conforme necessidade)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    # Verifica conectividade simples fazendo um select 1
    with engine.connect() as conn:
        conn.execute(text("select 1"))
    return {"status": "ok"}

@app.get("/categories")
def list_categories():
    # Exemplo simples consumindo tabela migrada pelo Flyway
    with engine.connect() as conn:
        rows = conn.execute(text("""
            select id, name, description, created_at, updated_at
            from product_categories
            order by id asc
        """)).mappings().all()
    return list(rows)

# Handler para AWS Lambda via API Gateway HTTP API
handler = Mangum(app)
