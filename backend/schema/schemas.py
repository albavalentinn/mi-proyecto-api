from pydantic import BaseModel
from typing import List, Optional

# ==========================================
# ESQUEMAS PARA VIDEOJUEGOS (GAMES)
# ==========================================

class GameBase(BaseModel):
    title: str
    genre: Optional[str] = None
    release_year: Optional[int] = None

# Esquema usado para crear un juego nuevo (requiere el ID del desarrollador)
class GameCreate(GameBase):
    developer_id: int

# Esquema completo para devolver el juego en las peticiones GET
class Game(GameBase):
    id: int
    developer_id: int

    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS PARA DESARROLLADORES (DEVELOPERS)
# ==========================================

class DeveloperBase(BaseModel):
    name: str
    country: Optional[str] = None

# Esquema para crear un desarrollador
class DeveloperCreate(DeveloperBase):
    pass

# Esquema completo que incluye la lista de juegos asociados (Relación 1:N)
class Developer(DeveloperBase):
    id: int
    games: List[Game] = []

    class Config:
        from_attributes = True