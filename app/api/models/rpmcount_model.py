from app import Base
from app.api.models import *

class RpmCountModel(Base, Mixin, TrackMixin):
    __tablename__ = "rpmcount"
    count= integer_column()
    output = integer_column()
    station = integer_column()
    location = text_column()
    deviceSerial = title_column()

