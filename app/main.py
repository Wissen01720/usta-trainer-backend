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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción restringir a tus dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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