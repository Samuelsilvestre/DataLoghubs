from src.infra.connection_db import engine
from sqlalchemy import text

try:
    # Cria uma conexão temporária
    with engine.connect() as connection:
        # Executa um comando simples para testar
        resultado = connection.execute(text("SELECT version();"))
        print("\n✅ Conexão realizada com sucesso!")
        print(f"Versão do banco: {resultado.scalar()}")
except Exception as e:
    print(f"\n❌ Erro ao conectar: {e}")