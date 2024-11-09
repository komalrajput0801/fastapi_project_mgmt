# includes sqlalchemy models
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from core.base_models import UUIDBase


class User(UUIDBase):
    __tablename__ = "users"

    first_name = Column(String(20))
    last_name = Column(String(20))
    email = Column(String(50), unique=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128))
    is_active = Column(Boolean, default=True)

    project = relationship("Project", back_populates="owner")

