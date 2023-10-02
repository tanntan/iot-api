from fastapi import APIRouter, Depends,Request
from sqlalchemy.orm import Session
from app import get_db
from app.api.schemas.rpmcount import RpmSchemas, RpmDetailSchemas, RpmWebhookSchema
from app.api.services.rpm_logic import RpmLogic
import json

router = APIRouter(
    prefix="/api/v1/rpm",
    tags=["rpm"],
    responses={404: {"description": "Not found"}}
)
default = RpmLogic()


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
async def print_messages(body: Request, db: Session = Depends(get_db)):
		try:
			data = await body.json()
        # Parse the JSON string into a JSON object
			json_data = json.loads(data['payload'])
			rpmModel = RpmSchemas(**json_data)
			return default.create(rpmModel, db)
		except json.JSONDecodeError as e:
				return {"error": "Invalid JSON format", "details": str(e)}
		
@router.get('/{item_id}')
async def get(item_id: int, db: Session = Depends(get_db)):
    return default.get_by_id(item_id, db)


@router.put('/{item_id}')
async def update(item_id: int, obj: RpmSchemas, db: Session = Depends(get_db)):
    return default.update(item_id, obj, db)


@router.delete('/{item_id}', )
async def delete(item_id: int, db: Session = Depends(get_db)):
    return default.delete(item_id, db)
