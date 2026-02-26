class HiringAppException(Exception):
    def __init__(self, name: str, message: str, status_code: int = 400):
        self.name = name
        self.message = message
        self.status_code = status_code

class UserNotFoundException(HiringAppException):
    def __init__(self, user_id: int):
        super().__init__("UserNotFound", f"User with id {user_id} not found", 404)

class EmailAlreadyExistsException(HiringAppException):
    def __init__(self, email: str):
        super().__init__("EmailAlreadyExists", f"User with email {email} already exists", 400)

class JobNotFoundException(HiringAppException):
    def __init__(self, job_id: int):
        super().__init__("JobNotFound", f"Job with id {job_id} not found", 404)

class ApplicationNotFoundException(HiringAppException):
    def __init__(self, application_id: int):
        super().__init__("ApplicationNotFound", f"Application with id {application_id} not found", 404)
