from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL para SQLite. Apunta al archivo que tienes en la raíz del proyecto.
SQLALCHEMY_DATABASE_URL = "sqlite:///./video_games.db"

# engine es el motor de conexión. El check_same_thread es un requisito específico de SQLite.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal será la clase que usaremos para crear sesiones de base de datos reales
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es la clase de la que heredarán nuestros modelos relacionales
Base = declarative_base()

# Función generadora para manejar las conexiones a la BBDD en cada petición a la API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()