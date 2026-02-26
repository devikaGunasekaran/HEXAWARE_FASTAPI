from sqlalchemy.orm import Session
from ..repositories.application_repository import ApplicationRepository
from ..repositories.user_repository import UserRepository
from ..repositories.job_repository import JobRepository
from ..schemas.application_schema import ApplicationCreate, ApplicationUpdate
from ..exceptions.custom_exceptions import (
    ApplicationNotFoundException, 
    UserNotFoundException, 
    JobNotFoundException
)

class ApplicationService:
    def __init__(self, db: Session):
        self.repository = ApplicationRepository(db)
        self.user_repository = UserRepository(db)
        self.job_repository = JobRepository(db)

    def get_application(self, application_id: int):
        application = self.repository.get_application(application_id)
        if not application:
            raise ApplicationNotFoundException(application_id)
        return application

    def get_applications(self, skip: int = 0, limit: int = 100):
        return self.repository.get_applications(skip, limit)

    def get_user_applications(self, user_id: int):
        if not self.user_repository.get_user(user_id):
            raise UserNotFoundException(user_id)
        return self.repository.get_user_applications(user_id)

    def create_application(self, application: ApplicationCreate):
        # Validate user and job exist
        if not self.user_repository.get_user(application.user_id):
            raise UserNotFoundException(application.user_id)
        if not self.job_repository.get_job(application.job_id):
            raise JobNotFoundException(application.job_id)
        
        return self.repository.create_application(application)

    def update_application_status(self, application_id: int, application: ApplicationUpdate):
        self.get_application(application_id) # Check if exists
        return self.repository.update_application_status(application_id, application.status)
