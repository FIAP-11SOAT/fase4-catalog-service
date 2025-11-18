from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db
from .routes.categories import router as categories_router
from .routes.products import router as products_router
from mangum import Mangum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Catalogo - Categories API", version="1.0.0")

@app.on_event("startup")
def on_startup():
	logger.info("🚀 Application starting up...")
	init_db()
	logger.info("✅ Application ready!")

app.include_router(categories_router)
app.include_router(products_router)

# CORS (ajuste allow_origins conforme necessidade)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get("/health")
def health():
	return {"status": "ok"}

# AWS Lambda handler (via Mangum)
handler = Mangum(app)

