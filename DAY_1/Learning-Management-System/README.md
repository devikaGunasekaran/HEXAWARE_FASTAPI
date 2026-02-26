# Learning Management System (LMS) - Backend

This project is a RESTful API for a Course Enrollment Platform built with **FastAPI** following **Clean Architecture** principles.

## Features
- **Course Management**: Create, view, and list courses.
- **Student Management**: Register and view student profiles.
- **Enrollment Management**: Enroll students in courses with validation (no duplicate enrollments).
- **In-Memory Storage**: Data is stored in-memory (no persistent database required as per requirements).
- **Auto-Documentation**: Swagger (OpenAPI) documentation available at `/docs`.

## Tech Stack
- **FastAPI**: Web framework.
- **Pydantic**: Data validation and schemas.
- **Uvicorn**: ASGI server.

## Project Structure
```
lms_app/
├── app/
│   ├── core/           # Configuration and In-memory Storage (db.py)
│   ├── schemas/        # Pydantic models (Input/Output Validation)
│   ├── repositories/   # Data Access Layer (List operations)
│   ├── services/       # Business Logic Layer (Business rules)
│   ├── controllers/    # Presentation Layer (API Routes)
│   ├── dependencies/   # Dependency Injection providers
│   ├── middleware/     # CORS and other middleware
│   └── main.py         # Entry point
├── requirements.txt
└── README.md
```

## Setup and Running

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   cd lms_app
   python -m app.main
   ```

3. **Explore the API**:
   - Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the Swagger UI.

## API Endpoints Summary

### Students
- `POST /students/` - Register a student.
- `GET /students/{id}` - Get student by ID.
- `GET /students/{id}/enrollments` - Get all courses a student is enrolled in.

### Courses
- `POST /courses/` - Create a course.
- `GET /courses/` - List all courses.
- `GET /courses/{id}` - Get course by ID.

### Enrollments
- `POST /enrollments` - Enroll a student in a course.
- `GET /enrollments` - List all enrollments.
- `GET /courses/{id}/enrollments` - List all students enrolled in a course.
