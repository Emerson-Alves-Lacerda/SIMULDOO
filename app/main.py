from fastapi import FastAPI
from app.connection.database import Base, engine
from app.routers import materias, questoes, alternativas, alunos, simulados, respostas, resultados

Base.metadata.create_all(bind=engine)

app = FastAPI()

#@app.on_event("startup")
#def reset_db():
#    Base.metadata.drop_all(bind=engine)
#    Base.metadata.create_all(bind=engine)


app.include_router(materias.router, prefix="/v1/materias", tags=["Materias"])
app.include_router(questoes.router, prefix="/v1/questoes", tags=["Questoes"])
app.include_router(alternativas.router, prefix="/v1/questao", tags=["Alternativas"])
app.include_router(alunos.router, prefix="/v1/aluno", tags=["Alunos"])
app.include_router(simulados.router, prefix="/v1/simulados", tags=["Simulados"])
app.include_router(respostas.router, prefix="/v1/resposta", tags=["Respostas"])
app.include_router(resultados.router, prefix="/v1/simulados", tags=["Resultados"])

