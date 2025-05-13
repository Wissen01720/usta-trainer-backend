from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import test
from app.routes import (
    exercises,
    users,
    submissions,
    auth,
    lessons,
    admin
)
from app.config import settings

app = FastAPI(
    title="USTA Trainer API",
    version="1.0.0",
    description="API para la plataforma educativa USTA Trainer"
)

# Configuración CORS
# Configuración CORS actualizada
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",  # Frontend en desarrollo (HTTP)
        "https://localhost:8080",  # Por si usas HTTPS local
        "https://tu-frontend-en-produccion.com"  # Dominio de producción
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Puedes especificar ["GET", "POST", ...] si prefieres
    allow_headers=["*"],  # O listar los headers específicos que usas
)

# Incluir todas las rutas
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(exercises.router)
app.include_router(submissions.router)
app.include_router(lessons.router)
app.include_router(admin.router)
app.include_router(test.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a USTA Trainer API"}