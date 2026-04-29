from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd

app = FastAPI()

df = pd.read_csv("prolongations.csv")
db = df.sort_values(by='id', ascending=True).to_dict(orient='records')


class FinancialData(BaseModel):
    id: int
    AM: str
    month: str


class FinancialShort(BaseModel):
    AM: str
    month: str


@app.get("/all-data")
async def get_all_data():
    """Возвращает все данные из базы"""
    return db


@app.get("/records/{id}")
async def get_data_by_id(id: int):
    """Возвращает данные по id"""
    for record in db:
        if record["id"] == id:
            return record
    raise HTTPException(status_code=404, detail="Записи с таким id не найдено")


@app.get("/filter", response_model=List[FinancialShort])
async def get_data_by_name(manager: str = None):
    """Возвращает данные по имени менеджера"""
    filtered_data = [record for record in db if record["AM"] == manager]
    if filtered_data:
        return filtered_data
    else:
        raise HTTPException(status_code=404, detail="Записей с таким менеджером не обнаружено =)")


@app.post("/new-data", status_code=201)
async def add_new_data(data: FinancialData):
    """Добавляет новые данные в базу"""
    db.append(data.dict())
    pd.DataFrame(db).to_csv("prolongations_new.csv", index=False)
    raise HTTPException(status_code=200, detail="Новые данные успешно сохранены")

