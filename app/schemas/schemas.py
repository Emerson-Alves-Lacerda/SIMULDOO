from pydantic import BaseModel
from typing import Optional
from typing import List

class MateriaBase(BaseModel):
    nome: str
    ano: int
    descricao: Optional[str] = None

class MateriaCreate(MateriaBase):
    pass

class MateriaOut(BaseModel):
    id: int
    nome: str
    ano: int
    descricao: str | None = None
    class Config:
        from_attributes = True

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
    simulado_id: int
    questao_id: int
    alternativas: List[int]

class RespostaOut(BaseModel):
    aluno: dict
    simulado_id: int
    questao_id: int
    corretas: bool
    class Config:
        orm_mode = True


class SimuladoCreate(BaseModel):
    nome: str

class SimuladoOut(BaseModel):
    id: int
    nome: str
    class Config:
        orm_mode = True

