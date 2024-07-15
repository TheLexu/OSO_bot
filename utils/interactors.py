from sqlalchemy.orm import Session

from db.engine import SessionLocal
from db.models import User


class BaseDBInteractor:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id):
        return self.db.query(User).filter(User.id == user_id).first()

db_interactor = BaseDBInteractor(db=SessionLocal())