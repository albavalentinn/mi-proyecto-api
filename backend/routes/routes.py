from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from schema import schemas
from controller import developer_controller, game_controller
from database.db import get_db

router = APIRouter()

# ==========================================
# RUTAS PARA DESARROLLADORES (DEVELOPERS)
# ==========================================

@router.post("/developers/", response_model=schemas.Developer, status_code=status.HTTP_201_CREATED)
def create_developer(developer: schemas.DeveloperCreate, db: Session = Depends(get_db)):
    return developer_controller.create_developer(db=db, developer=developer)

@router.get("/developers/", response_model=List[schemas.Developer])
def read_developers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return developer_controller.get_developers(db, skip=skip, limit=limit)

@router.get("/developers/{developer_id}", response_model=schemas.Developer)
def read_developer(developer_id: int, db: Session = Depends(get_db)):
    db_developer = developer_controller.get_developer(db, developer_id=developer_id)
    if db_developer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Desarrollador no encontrado")
    return db_developer

@router.put("/developers/{developer_id}", response_model=schemas.Developer)
def update_developer(developer_id: int, developer: schemas.DeveloperCreate, db: Session = Depends(get_db)):
    db_developer = developer_controller.update_developer(db, developer_id, developer)
    if db_developer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Desarrollador no encontrado")
    return db_developer

@router.delete("/developers/{developer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_developer(developer_id: int, db: Session = Depends(get_db)):
    db_developer = developer_controller.delete_developer(db, developer_id)
    if db_developer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Desarrollador no encontrado")
    return None

# ==========================================
# RUTAS PARA VIDEOJUEGOS (GAMES)
# ==========================================

@router.post("/games/", response_model=schemas.Game, status_code=status.HTTP_201_CREATED)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    # Primero verificamos que el desarrollador asociado realmente exista
    db_dev = developer_controller.get_developer(db, developer_id=game.developer_id)
    if db_dev is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El desarrollador indicado no existe")
    return game_controller.create_game(db=db, game=game)

@router.get("/games/", response_model=List[schemas.Game])
def read_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return game_controller.get_games(db, skip=skip, limit=limit)

@router.get("/games/{game_id}", response_model=schemas.Game)
def read_game(game_id: int, db: Session = Depends(get_db)):
    db_game = game_controller.get_game(db, game_id=game_id)
    if db_game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Videojuego no encontrado")
    return db_game

@router.put("/games/{game_id}", response_model=schemas.Game)
def update_game(game_id: int, game: schemas.GameCreate, db: Session = Depends(get_db)):
    db_game = game_controller.update_game(db, game_id, game)
    if db_game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Videojuego no encontrado")
    return db_game

@router.delete("/games/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(game_id: int, db: Session = Depends(get_db)):
    db_game = game_controller.delete_game(db, game_id)
    if db_game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Videojuego no encontrado")
    return None