from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URI

# Ao criar a Session, desabilitamos o expire_on_commit para que
# objetos retornados após commit não sejam automáticamente expirados
# e evitem erros do tipo "Instance ... is not bound to a Session"
engine = create_engine(DB_URI, connect_args={"check_same_thread": False})
# expire_on_commit=False mantém os atributos carregados acessíveis
# mesmo após o commit (útil para pequenos projetos e para evitar acesso
# a atributos lazy depois que a sessão é fechada). Em alternativas
# melhores, converta/serialize objetos antes de fechar a sessão.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
