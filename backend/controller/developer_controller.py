from sqlalchemy.orm import Session
from model import models
from schema import schemas

# ==========================================
# READ: Obtener todos los desarrolladores
# ==========================================
def get_developers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Developer).offset(skip).limit(limit).all()

# ==========================================
# READ: Obtener un desarrollador por ID
# ==========================================
def get_developer(db: Session, developer_id: int):
    return db.query(models.Developer).filter(models.Developer.id == developer_id).first()

# ==========================================
# CREATE: Crear un nuevo desarrollador
# ==========================================
def create_developer(db: Session, developer: schemas.DeveloperCreate):
    # Creamos la instancia del modelo de base de datos usando los datos validados del esquema
    db_developer = models.Developer(name=developer.name, country=developer.country)
    db.add(db_developer)
    db.commit()
    db.refresh(db_developer) # Refrescamos para obtener el ID generado por la base de datos
    return db_developer

# ==========================================
# UPDATE: Actualizar un desarrollador
# ==========================================
def update_developer(db: Session, developer_id: int, developer_data: schemas.DeveloperCreate):
    db_developer = get_developer(db, developer_id)
    if db_developer:
        db_developer.name = developer_data.name
        db_developer.country = developer_data.country
        db.commit()
        db.refresh(db_developer)
    return db_developer

# ==========================================
# DELETE: Borrar un desarrollador
# ==========================================
def delete_developer(db: Session, developer_id: int):
    db_developer = get_developer(db, developer_id)
    if db_developer:
        db.delete(db_developer)
        db.commit()
    return db_developer