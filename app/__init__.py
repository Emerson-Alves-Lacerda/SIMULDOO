from app.connection.database import Base, engine
from app.models import models

# Cria todas as tabelas no banco conforme os modelos
Base.metadata.create_all(bind=engine)

print("✅ Banco de dados recriado com sucesso.")
