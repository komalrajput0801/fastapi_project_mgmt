from typing import Optional, List
import uuid
from typing import NewType
from pydantic import BaseModel

from user.models import User

from user.schemas import UserID, UserOut

ProjectID = NewType("ProjectID", uuid.UUID)

class ProjectBase(BaseModel):
    name: str


class ProjectCreate(ProjectBase):
    owner_id: UserID = Optional


class CollaboratorSchema(BaseModel):
    ids: List[UserID]


class ProjectOut(ProjectBase):
    id: ProjectID
    collaborators: List[UserOut]

    class Config:
        orm_mode = True
