# Contains CRUD operations
from typing import Any, Dict, List, Union

from core.crud_base import CRUDBase
from sqlalchemy.orm import Session
from user.exceptions import UserAlreadyExists, UserNotFound
from user.models import User
from user.schemas import UserBase, UserIn, UserID
from user.utils import get_hashed_password


class CRUDUser(CRUDBase[User, UserIn, UserIn]):
    def create(self, db: Session, obj_in: UserIn) -> User:
        db_user = db.query(User).filter(User.email == obj_in.email).first()
        if db_user:
            raise UserAlreadyExists()

        # hash the password before saving it to database
        obj_in.password = get_hashed_password(obj_in.password)
        return super().create(db, obj_in=obj_in)

    def get_user_by_username(self, db: Session, username: str) -> User:
        return db.query(User).filter(User.username == username).first()

    def get_multi(
        self, db: Session, page_size: int = 10, page_num: int = 1, search: str = None
    ) -> List[User]:
        if search:
            return (
                db.query(User)
                .filter(User.full_name.contains(search) | User.email.contains(search))
                .offset((page_num - 1) * page_size)
                .limit(page_size)
                .all()
            )
        return super().get_multi(db, offset=(page_num - 1) * page_size, limit=page_size)

    def update(self, db: Session, user_id: UserID, obj_in: Union[UserBase, Dict[str, Any]]) -> User:
        db_user = db.query(User).get(user_id)
        if not db_user:
            raise UserNotFound()
        # checks if email passed in update data already exists
        # excluding the email of user obj
        user_exists = (
            db.query(User)
            .filter(User.email == obj_in.email)
            .filter(User.email != db_user.email)  # works as exclude
            .first()
        )
        if user_exists:
            raise UserAlreadyExists()
        return super().update(db, db_obj=db_user, obj_in=obj_in)


user = CRUDUser(User)
