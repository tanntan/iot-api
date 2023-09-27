from app.api.schemas.devices import DeviceSchema
from app.api.services.base_logic import BaseLogic
from app.api.models.device_model import DeviceModel


class DeviceLogic(BaseLogic):

    def __init__(self):
        super().__init__(DeviceModel, DeviceSchema)