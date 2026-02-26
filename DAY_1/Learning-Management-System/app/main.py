from fastapi import FastAPI
from app.controllers import student_controller, course_controller, enrollment_controller
from app.middleware.cors import add_cors_middleware

app = FastAPI(
    title="LMS - Course Enrollment Platform",
    description="A backend system for managing courses, students, and enrollments using Clean Architecture.",
    version="1.0.0"
)

# Add Middleware
add_cors_middleware(app)

# Include Routers
app.include_router(student_controller.router)
app.include_router(course_controller.router)
app.include_router(enrollment_controller.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the LMS API. Visit /docs for documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
