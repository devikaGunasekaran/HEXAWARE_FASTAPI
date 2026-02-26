# 🗓️ Event Management API

A clean-architecture FastAPI backend for managing events and participants using **in-memory storage**.

---

## 📁 Project Structure

```
event_management_api/
│
├── app/
│   └── main.py                    # FastAPI app entry point
│
├── controllers/
│   ├── event_controller.py        # Event route definitions
│   └── participant_controller.py  # Participant route definitions
│
├── services/
│   ├── event_service.py           # Event business logic
│   └── participant_service.py     # Participant business logic
│
├── repositories/
│   ├── event_repository.py        # In-memory event storage
│   └── participant_repository.py  # In-memory participant storage
│
├── schemas/
│   ├── event_schema.py            # Pydantic models for events
│   └── participant_schema.py      # Pydantic models for participants
│
├── dependencies/
│   └── service_dependency.py      # Dependency injection
│
├── middleware/
│   └── cors_middleware.py         # CORS configuration
│
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the server

```bash
uvicorn app.main:app --reload
```

### 3. Open Swagger UI

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📡 API Endpoints

### Events

| Method | Endpoint             | Description                          |
|--------|----------------------|--------------------------------------|
| POST   | `/events`            | Create a new event                   |
| GET    | `/events`            | List all events                      |
| GET    | `/events/{id}`       | Get event by ID                      |
| GET    | `/events?location=X` | Filter events by location            |

### Participants

| Method | Endpoint               | Description                          |
|--------|------------------------|--------------------------------------|
| POST   | `/participants`        | Register a participant for an event  |
| GET    | `/participants/{id}`   | Get participant by ID                |

---

## 🧠 Business Rules

- ❌ Duplicate event names are **not allowed**
- ❌ Participant email must be **unique**
- ❌ Registration is **rejected** if event capacity is full
- ❌ Registration fails if the **event does not exist**

---

## 🏛️ Architecture

```
Client
  ↓
Controller Layer  →  (HTTP Routes, no business logic)
  ↓
Service Layer     →  (Business rules & validation)
  ↓
Repository Layer  →  (In-memory data storage)
  ↓
In-Memory Lists
```
