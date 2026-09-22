from sqlalchemy.orm import Session
from model import models
from schema import schemas

# ==========================================
# READ: Obtener todos los videojuegos
# ==========================================
def get_games(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Game).offset(skip).limit(limit).all()

# ==========================================
# READ: Obtener un videojuego por ID
# ==========================================
def get_game(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.id == game_id).first()

# ==========================================
# CREATE: Crear un nuevo videojuego
# ==========================================
def create_game(db: Session, game: schemas.GameCreate):
    # Pasamos también el developer_id para vincular el juego a su creador
    db_game = models.Game(
        title=game.title,
        genre=game.genre,
        release_year=game.release_year,
        developer_id=game.developer_id
    )
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

# ==========================================
# UPDATE: Actualizar un videojuego
# ==========================================
def update_game(db: Session, game_id: int, game_data: schemas.GameCreate):
    db_game = get_game(db, game_id)
    if db_game:
        db_game.title = game_data.title
        db_game.genre = game_data.genre
        db_game.release_year = game_data.release_year
        db_game.developer_id = game_data.developer_id
        db.commit()
        db.refresh(db_game)
    return db_game

# ==========================================
# DELETE: Borrar un videojuego
# ==========================================
def delete_game(db: Session, game_id: int):
    db_game = get_game(db, game_id)
    if db_game:
        db.delete(db_game)
        db.commit()
    return db_game
