from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import engine
from model import models
from routes import routes

# Esta línea le dice a SQLAlchemy que cree las tablas en SQLite basándose en models.py
models.Base.metadata.create_all(bind=engine)

# Inicializamos la aplicación FastAPI con metadatos para la documentación automática
app = FastAPI(
    title="API de Videojuegos y Desarrolladores",
    description="API REST modular con relaciones 1:N entre Desarrolladores y Videojuegos.",
    version="1.0.0"
)

# Configuración de CORS: Vital para permitir que el frontend (HTML/JS) haga peticiones a esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen (ideal para desarrollo local)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],
)

# Añadimos todas las rutas que definimos en routes.py
app.include_router(routes.router)