from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session


# Base class for CRUD operations
class BaseLogic:
    def __init__(self, model, schema):
        self.model = model
        self.schema = schema

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def get_by_id(self, item_id: int, db: Session):
        obj = db.query(self.model).filter(self.model.id == item_id).first()
        if not obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        return obj

    def create(self, schema, db: Session):
        obj = self.model(**schema.dict())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, item_id: int, schema: BaseModel, db: Session):
        obj = self.get_by_id(item_id, db)
        for field, value in schema.dict(exclude_unset=True).items():
            setattr(obj, field, value)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, item_id: int, db: Session) -> None:
        obj = self.get_by_id(item_id, db)
        db.delete(obj)
        db.commit()
