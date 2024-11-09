from fastapi import APIRouter
from fastapi.params import Depends, Security
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from typing import List
from core.dependencies import get_db
from project.crud import project
from project.schemas import ProjectOut, ProjectBase, ProjectCreate, ProjectID, CollaboratorSchema
from user.models import User
from user.utils import get_current_user

router = APIRouter(prefix="/project")


@cbv(router)
class ProjectCBV:
    session: Session = Depends(get_db)
    logged_in_user: User = Depends(get_current_user)

    @router.post("/", response_model=ProjectOut)
    def create_project(self, project_data: ProjectCreate):
        """Creates new project. Only logged in users can create projects"""
        project_data.owner_id = self.logged_in_user.id
        return project.create(self.session, obj_in=project_data)


    @router.get("/", response_model=List[ProjectOut])
    def get_projects_of_user(self):
        """Returns project of users created by them or projects in which they are collaborators"""
        return project.get_projects_of_user(self.session, self.logged_in_user.id)


    @router.get("/{uuid}", response_model=ProjectOut)
    def get_project_by_uuid(self, uuid: ProjectID):
        return project.get(self.session, uuid, self.logged_in_user.id)


    @router.post("/{uuid}/add", response_model=ProjectOut)
    def add_collaborators(self, uuid: ProjectID, collab_ids: CollaboratorSchema):
        return project.add_collaborators(self.session, uuid, self.logged_in_user.id, collab_ids)


    @router.put("/{uuid}", response_model=ProjectOut)
    def edit_project(self, uuid: ProjectID, project_data: ProjectBase):
        return project.update(self.session, user_id=self.logged_in_user.id, project_id=uuid, obj_in=project_data)

    @router.delete("/{uuid}")
    def delete_project(self, uuid: ProjectID):
        project.remove(self.session, id=uuid)
        return {"message": "Project Deleted successfully"}