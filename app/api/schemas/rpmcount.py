from datetime import datetime

from pydantic import BaseModel
class RpmWebhookSchema(BaseModel):
    username: str
    topic: str
    timestamp: int
    qos: int
    publish_received_at: int
    pub_props: dict
    peerhost: str
    payload: dict
    node: str
    metadata: dict
    id: str
    from_username: str
    from_clientid: str
    flags: dict
    event: str
    clientid: str

class RpmSchemas(BaseModel):

    count: int
    output: int
    station: int
    location: str
    deviceSerial:str

    class Config:
        orm_mode = True


class RpmCreateSchema(RpmSchemas):
    pass


class RpmUpdateSchema(RpmSchemas):
    id: int


class RpmDetailSchemas(RpmSchemas):
    id: int
    created_date: datetime
    created_by: str
    updated_date: datetime
    updated_by: str

    class Config:
        orm_mode = True
