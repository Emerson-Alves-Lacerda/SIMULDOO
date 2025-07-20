from pydantic import BaseModel
from typing import Optional
from typing import List

class MateriaBase(BaseModel):
    nome: str
    ano: int
    descricao: Optional[str] = None

class MateriaCreate(MateriaBase):
    pass

class MateriaOut(MateriaBase):
    id: int
    class Config:
        orm_mode = True

class QuestaoBase(BaseModel):
    enunciado: str
    nivel: int
    materia: int
    total_correta: int

class QuestaoCreate(QuestaoBase):
    pass

class QuestaoOut(QuestaoBase):
    id: int
    status: bool
    class Config:
        orm_mode = True

class AlternativaBase(BaseModel):
    descricao: str
    correto: bool

class AlternativaCreate(AlternativaBase):
    pass

class AlternativaOut(AlternativaBase):
    id: int
    class Config:
        orm_mode = True

# Usuário
class UsuarioCreate(BaseModel):
    nome: str
    matricula: str

class UsuarioOut(BaseModel):
    id: int
    nome: str
    matricula: str
    total_simulados: Optional[int] = 0

    class Config:
        orm_mode = True

# Resposta
class RespostaCreate(BaseModel):
    id_aluno: int
    questao_id: int
    alternativas: List[int]
