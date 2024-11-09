from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, String, ForeignKey, Table, Integer
from sqlalchemy.orm import relationship

from core.base_models import UUIDBase
from database import Base

collaborator_table = Table(
    "collaborators",
    Base.metadata,
    Column("project_id", ForeignKey("project.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True)
)


class Project(UUIDBase):
    __tablename__ = "project"

    name = Column(String(50), unique=True)
    owner_id = Column(GUID, ForeignKey("users.id"))
    owner = relationship("User", back_populates="project")
    collaborators = relationship("User", secondary=collaborator_table, backref="users")