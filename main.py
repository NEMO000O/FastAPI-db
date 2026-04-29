from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import database
from pydantic import BaseModel

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()


class CreateData(BaseModel):
    manager_name: str
    revenue: float


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/data")
def get_all_data(db: Session = Depends(get_db)):
    """Получение всех данных из базы"""
    data = db.query(models.Prolongations).all()
    return data


@app.get("/projects/{project_id}")
def get_data_by_id(project_id: int, db: Session = Depends(get_db)):
    """Возвращает данные по id"""
    data = db.query(models.Prolongations).filter(models.Prolongations.id == project_id).first()  # Обязательно указывай .first() или .all(), иначе провалишься в рекурсию
    if data:
        return data
    else:
        raise HTTPException(status_code=404, detail=f"Проект с id {project_id} не найден")


@app.post("/data/create", status_code=201)
def create_data(project_data: CreateData, db: Session = Depends(get_db)):
    """Добавление новой записи в базу"""
    new_project = models.Prolongations(manager_name=project_data.manager_name, revenue=project_data.revenue)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)


@app.delete("/projects/del/{project_id}")
def delete_data_by_id(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Prolongations).filter(models.Prolongations.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail=f"Проект с id {project_id} не найден")
    db.delete(project)
    db.commit()
    return None


