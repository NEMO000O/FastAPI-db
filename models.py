from sqlalchemy import Column, Integer, String, Float
from database import Base


class Prolongations(Base):
    __tablename__ = "prolongations"

    id = Column(Integer, primary_key=True, index=True)
    manager_name = Column(String, index=True)
    revenue = Column(Float)
    status = Column(String, default="active")
