# Loan Application & Approval Management System API

A Clean Architecture implementation of a loan processing workflow using FastAPI and in-memory storage.

## Features
- Submit loan applications with automatic eligibility checks.
- View application status and list all applications.
- Approve or reject loans with business rule validation.
- Clean Architecture (Controller -> Service -> Repository).

## Tech Stack
- **FastAPI**: Modern, fast (high-performance) web framework for building APIs.
- **Pydantic**: Data validation and settings management.
- **In-Memory Storage**: Simple list-based storage for persistence during runtime.

## Project Structure
```
loan_app/
├── app/
│   ├── main.py
│   ├── core/           # Configuration
│   ├── models/         # In-memory data models
│   ├── schemas/        # Request/Response models
│   ├── repositories/   # Data access layer
│   ├── services/       # Business logic layer
│   ├── controllers/    # API routes
│   ├── dependencies/   # DI providers
│   └── middleware/     # CORS etc.
├── requirements.txt
└── README.md
```

## Setup & Running

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   cd loan_app
   python -m app.main
   ```

3. **API Documentation**:
   Once running, visit `http://localhost:8000/docs` for interactive Swagger documentation.

## Business Rules
- **Eligibility**: Loan amount must not exceed `income * 10`.
- **Auto-Rejection**: Applications exceeding eligibility are rejected automatically on submission.
- **Transitions**: Only `PENDING` loans can be approved or rejected.
- **Manual Approval Check**: Re-validates eligibility during the manual approval process.
