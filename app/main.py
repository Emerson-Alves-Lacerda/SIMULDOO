from fastapi import FastAPI
from app.connection.database import Base, engine
from app.routers import materias, questoes, alternativas

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(materias.router, prefix="/v1/materias", tags=["Materias"])
app.include_router(questoes.router, prefix="/v1/questoes", tags=["Questoes"])
app.include_router(alternativas.router, prefix="/v1/questao", tags=["Alternativas"])
