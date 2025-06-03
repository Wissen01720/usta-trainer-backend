from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
    auth, 
    users,
    submissions,
    lessons,
    admin,
    progress,   # <--- agrega la coma aquí
    teacher
)
from app.config import settings

app = FastAPI(
    title="USTA Trainer API",
    version="1.0.0",
    description="API para la plataforma educativa USTA Trainer"
)

# Configuración CORS
origins = [
    "http://localhost:8080",
    "http://localhost:3000",
    "https://virtualjudge.onrender.com",
    "https://tu-frontend-en-produccion.com",
    "https://usta-trainer-77sm026fn-edgards-projects-2f318633.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prefijo API v1
api_prefix = "/api/v1"

# Incluir rutas con prefijo
app.include_router(auth.router, prefix=api_prefix)
app.include_router(users.router, prefix=api_prefix)
app.include_router(submissions.router, prefix=api_prefix)
app.include_router(lessons.router, prefix=api_prefix)
app.include_router(admin.router, prefix=api_prefix)
app.include_router(progress.router, prefix=api_prefix)
app.include_router(teacher.router, prefix=api_prefix)

@app.get("/")
def root():
    return {"message": "Bienvenido a USTA Trainer API"}

@app.get(api_prefix)
def api_root():
    return {"message": "API v1 Endpoint"}