# tests/conftest.py
import pytest
from app.connection.database import Base, engine

@pytest.fixture(scope="session", autouse=True)
def initialize_db():
    """
    Antes de tudo, derruba e recria todas as tabelas no banco apontado
    por engine. Garante que o esquema de modelo e o DB estejam
    sempre sincronizados.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
