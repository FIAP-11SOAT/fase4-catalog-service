from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db
from .routes.categories import router as categories_router

app = FastAPI(title="Catalogo - Categories API", version="1.0.0")

@app.on_event("startup")
def on_startup():
	init_db()

app.include_router(categories_router)

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

