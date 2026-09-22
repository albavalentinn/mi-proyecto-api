from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Developer(Base):
    __tablename__ = "developers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    country = Column(String)

    # Relación: Un desarrollador tiene muchos juegos.
    # cascade="all, delete-orphan" asegura la integridad referencial si se borra un desarrollador.
    games = relationship("Game", back_populates="developer", cascade="all, delete-orphan")


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    genre = Column(String)
    release_year = Column(Integer)
    
    # Clave foránea que relaciona este juego con un desarrollador específico
    developer_id = Column(Integer, ForeignKey("developers.id"), nullable=False)

    # Relación inversa para poder acceder a los datos del desarrollador desde el juego
    developer = relationship("Developer", back_populates="games")