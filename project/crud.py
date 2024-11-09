import uuid

from typing import List, Any, Optional, Union, Dict

from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from core.crud_base import CRUDBase
from project.exceptions import ProjectAlreadyExists
from project.models import Project
from project.schemas import ProjectBase, ProjectCreate, CollaboratorSchema
from user.models import User


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectBase]):
    def create(self, db: Session, obj_in: ProjectCreate) -> Project:
        db_proj = db.query(Project).filter(Project.name == obj_in.name).first()
        if db_proj:
            raise ProjectAlreadyExists()
        return super().create(db, obj_in=obj_in)

    def get_projects_of_user(self, db:Session, userid: int) -> List[Project]:
    	"""Returns project of users created by them or projects in which they are collaborators"""
    	# return db.query(Project, Project.collaborators).join(Project.collaborators).filter(Project.collaborators.user_id.in_([userid])).all()
    	return db.query(Project).filter(Project.owner_id == userid).all()

    def get(self, db: Session, id: uuid.UUID, user_id: int) -> Optional[Project]:
        db_obj = db.query(Project).filter(Project.id == id, Project.owner_id == user_id).first()
        if not db_obj:
            raise HTTPException(
            	status_code=status.HTTP_404_NOT_FOUND,
            	detail="Project ID not found or project does not belong to logged in user"
        	)
        return db_obj

    def add_collaborators(self, db: Session, id: uuid.UUID, user_id: int, collab_ids: CollaboratorSchema) -> Project:
    	proj = self.get(db, id, user_id)
    	if proj:
    		users = db.query(User).filter(User.id.in_(collab_ids.ids)).all()
    		proj.collaborators.extend(users)
    		db.add(proj)
    		db.commit()
    		db.refresh(proj)
    		return proj

    def update(self, db: Session, user_id: uuid.UUID, project_id: uuid.UUID, obj_in: Union[ProjectBase, Dict[str, Any]]) -> Project:
        db_proj = self.get(db, project_id, user_id)
        # checks if project name passed in update data already exists
        # excluding the project name of project obj
        proj_exists = (
            db.query(Project)
            .filter(Project.name == obj_in.name)
            .filter(Project.name != db_proj.name)  # works as exclude
            .first()
        )
        if proj_exists:
            raise ProjectAlreadyExists()
        return super().update(db, db_obj=db_proj, obj_in=obj_in)


project = CRUDProject(Project)
