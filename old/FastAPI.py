from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd

app = FastAPI()


class FinancialData(BaseModel):
    project_id: int
    manager: str
    january_2023: float = 0.0
    february_2023: float = 0.0
    March_2023: float = 0.0
    status: str = "active"


db = [
    {"project_id": 1, "manager": "Винзавод Терентий", "january_2023": 16.7,
     "february_2023": 54.7, "March_2023": 93.6, "status": "stop"},
    {"project_id": 2, "manager": "Сергей Михалков", "january_2023": 72.3,
     "february_2023": 14.6, "March_2023": 100.0, "status": "active"},
    {"project_id": 3, "manager": "Винзавод Терентий", "january_2023": 92.7,
     "february_2023": 45.7, "March_2023": 83.6, "status": "active"}
]


@app.get("/financial")
async def get_all_records():
    """Возвращает все записи из таблицы"""
    return db


@app.get("/financial/total_january")
async def return_total_january():
    """Считает сумму всех отгрузок за Январь"""
    total = sum(item["january_2023"] for item in db)
    return total


@app.get("/financial/{project_id}")
async def get_project_by_id(project_id: int):
    """Возвращает информацию о проекте по ID"""
    for record in db:
        if record["project_id"] == project_id:
            return record
    raise HTTPException(status_code=404, detail="Проект с таким ID не найден в базе")


@app.get("/financial/{project_id}/status")
async def get_project_status_by_id(project_id: int):
    """Возвращает статус проекта по ID"""
    for record in db:
        if record["project_id"] == project_id:
            return {"project_id": project_id, "status": record["status"]}
    return {"error": "Проект не найден"}


@app.get("/financial/search/manager")
async def get_project_by_manager_name(manager: str):
    """Возвращает проекты конкретного менеджера (по имени)"""
    result = [record for record in db if record["manager"] == manager]
    if len(result) != 0:
        return result
    else:
        return {"error": "Проекты не найдены"}


@app.post("/financial/add")
async def add_record(record: FinancialData):
    """Добавляет новый проект в базу"""
    db.append(record.dict())
    return {"INFO": "Проект успешно добавлен"}


@app.post("/financial/stop-project")
async def stop_projects(projects_id: List[int]):
    """Изменяет статус проектов на 'стоп'"""
    for record in db:
        if record["project_id"] == projects_id:
            record["status"] = "stop"
    return {"INFO": "Изменения внесены"}
