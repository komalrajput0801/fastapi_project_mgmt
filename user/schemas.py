# includes pydantic models
import uuid
from typing import NewType

from pydantic import BaseModel

UserID = NewType("UserID", uuid.UUID)


# class CustomBaseModel(BaseModel):
#     """
#     CustomBaseModel created to provide functionality of passing two attributes
#     include and exclude which will include and exclude fields from the inherited model
#     """
#     def json(self, **kwargs):
#         include = getattr(self.Config, "include", set())
#         if len(include) == 0:
#             include = None
#         exclude = getattr(self.Config, "exclude", set())
#         if len(exclude) == 0:
#             exclude = None
#         return super().json(include=include, exclude=exclude, **kwargs)


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    username: str


# model with fields needed at time of creation
class UserIn(UserBase):
    password: str


# model with fields at time of reading data
class UserOut(UserBase):
    id: UserID
    is_active: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
