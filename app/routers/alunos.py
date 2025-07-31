from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.connection.database import SessionLocal
from app.models.models import Usuario, AlunoSimulado
from app.schemas.schemas import UsuarioCreate, UsuarioOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/", response_model=UsuarioOut)
def criar_aluno(aluno: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter_by(matricula=aluno.matricula).first():
        raise HTTPException(400, detail="Matrícula já cadastrada.")
    novo = Usuario(**aluno.dict())
    db.add(novo); db.commit(); db.refresh(novo)
    return novo

@router.get("/", response_model=List[UsuarioOut])
def listar_alunos(db: Session = Depends(get_db)):
    alunos = db.query(Usuario).all()
    resultados = []
    for a in alunos:
        total = db.query(AlunoSimulado).filter_by(alunos_id=a.id).count()
        resultados.append(UsuarioOut(**a.__dict__, total_simulados=total))
    return resultados

@router.get("/{id}/", response_model=UsuarioOut)
def aluno_detalhe(id: int, db: Session = Depends(get_db)):
    aluno = db.query(Usuario).get(id)
    if not aluno:
        raise HTTPException(404, "Aluno não encontrado.")
    total = db.query(AlunoSimulado).filter_by(alunos_id=aluno.id).count()
    return UsuarioOut(**aluno.__dict__, total_simulados=total)
