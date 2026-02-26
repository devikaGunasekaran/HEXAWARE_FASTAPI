from sqlalchemy.orm import Session
from ..models.application import Application
from ..schemas.application_schema import ApplicationCreate

class ApplicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_application(self, application_id: int):
        return self.db.query(Application).filter(Application.id == application_id).first()

    def get_applications(self, skip: int = 0, limit: int = 100):
        return self.db.query(Application).offset(skip).limit(limit).all()

    def get_user_applications(self, user_id: int):
        return self.db.query(Application).filter(Application.user_id == user_id).all()

    def create_application(self, application: ApplicationCreate):
        db_application = Application(**application.dict())
        self.db.add(db_application)
        self.db.commit()
        self.db.refresh(db_application)
        return db_application

    def update_application_status(self, application_id: int, status: str):
        db_application = self.get_application(application_id)
        if db_application:
            db_application.status = status
            self.db.commit()
            self.db.refresh(db_application)
        return db_application
