from datetime import datetime

from pydantic import BaseModel

class DeviceSchema(BaseModel):

    name: str
    serial: str
    status: bool
    lineName: str
    stationId: int
    remark: str
    description: str
    version: str

    class Config:
        orm_mode = True


class DeviceCreateSchema(DeviceSchema):
    pass


class DeviceUpdateSchema(DeviceSchema):
    id: int


class DeviceDetailSchemas(DeviceSchema):
    id: int
    created_date: datetime
    created_by: str
    updated_date: datetime
    updated_by: str

    class Config:
        orm_mode = True
