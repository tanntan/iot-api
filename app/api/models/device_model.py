from app import Base
from app.api.models import *

class DeviceModel(Base, Mixin, TrackMixin):
    __tablename__ = "devices"
    
    name = title_column(unique=True)
    serial = code_column(unique=True)
    status = boolean_column()
    lineName = text_column()
    stationId = integer_column()
    remark = title_column()
    version = title_column()
    description = note_column()
