from app.api.schemas.rpmcount import RpmSchemas
from app.api.services.base_logic import BaseLogic
from app.api.models.rpmcount_model import RpmCountModel


class RpmLogic(BaseLogic):

    def __init__(self):
        super().__init__(RpmCountModel, RpmSchemas)