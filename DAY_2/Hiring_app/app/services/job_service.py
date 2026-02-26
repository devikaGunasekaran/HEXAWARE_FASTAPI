from sqlalchemy.orm import Session
from ..repositories.job_repository import JobRepository
from ..repositories.user_repository import UserRepository
from ..schemas.job_schema import JobCreate, JobUpdate
from ..exceptions.custom_exceptions import JobNotFoundException, UserNotFoundException

class JobService:
    def __init__(self, db: Session):
        self.repository = JobRepository(db)
        self.user_repository = UserRepository(db)

    def get_job(self, job_id: int):
        job = self.repository.get_job(job_id)
        if not job:
            raise JobNotFoundException(job_id)
        return job

    def get_jobs(self, skip: int = 0, limit: int = 10):
        return self.repository.get_jobs(skip, limit)

    def create_job(self, job: JobCreate):
        # Validate company exists
        if not self.user_repository.get_user(job.company_id):
            raise UserNotFoundException(job.company_id)
        return self.repository.create_job(job)

    def update_job(self, job_id: int, job: JobUpdate):
        self.get_job(job_id) # Check if exists
        return self.repository.update_job(job_id, job.dict(exclude_unset=True))

    def delete_job(self, job_id: int):
        self.get_job(job_id) # Check if exists
        return self.repository.delete_job(job_id)
