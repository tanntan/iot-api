from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import get_db
from app.api.schemas.devices import DeviceSchema, DeviceDetailSchemas
from app.api.services.device_logic import DeviceLogic
router = APIRouter(
    prefix="/api/v1/devices",
    tags=["devices"],
    responses={404: {"description": "Not found"}}
)
default = DeviceLogic()


@router.get(
    '/',
    response_description="devices description",
    summary="devices summary",
    description="descriptions"
)
async def get_all(db: Session = Depends(get_db)):
    return default.get_all(db)


@router.post(
    '/',
    response_description="devices description",
    summary="devices summary",
    description="descriptions"
)
async def create(obj: DeviceSchema, db: Session = Depends(get_db)):
    return default.create(obj, db)


@router.get('/{item_id}')
async def get(item_id: int, db: Session = Depends(get_db)):
    return default.get_by_id(item_id, db)


@router.put('/{item_id}')
async def update(item_id: int, obj: DeviceSchema, db: Session = Depends(get_db)):
    return default.update(item_id, obj, db)


@router.delete('/{item_id}', )
async def delete(item_id: int, db: Session = Depends(get_db)):
    return default.delete(item_id, db)
