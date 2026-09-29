# Hospital Management API

A RESTful backend API for managing hospital operations, built with **FastAPI** and **SQLAlchemy**.

The API provides administrative management for patients, doctors, staff, appointments, and medical records, with authentication, authorization, relational database modeling, and database migrations.

> **Project Status:** Core backend functionality is complete. PostgreSQL, Docker, production configuration, and cloud deployment are the next development stages.

---

## Features

- RESTful API built with FastAPI
- SQLAlchemy ORM for database interaction
- Relational database design using primary and foreign keys
- JWT-based authentication
- Bcrypt password hashing
- Role-based authorization
- Primary Admin and Normal Admin privilege system
- Protected API routes
- Pydantic request and response validation
- SQLAlchemy model relationships
- Alembic database migrations
- Centralized exception handling
- Environment-based configuration
- Interactive API documentation with Swagger UI
- OpenAPI documentation with ReDoc

---

## Architecture

The application follows a layered backend architecture to keep API logic, validation, database operations, and security concerns separated.

```text
Routers
   ↓
Schemas
   ↓
Models
   ↓
Database
```

### Routers

Routers handle HTTP requests and define API endpoints.

The application contains separate routers for:

- Authentication
- Patients
- Doctors
- Staff
- Appointments
- Medical Records

### Schemas

Pydantic schemas are responsible for:

- Request validation
- Response serialization
- Defining API response structures
- Controlling which data is exposed to API clients

### Models

SQLAlchemy models represent the database entities and their relationships.

### Utilities

Utility modules handle common backend concerns such as:

- Database sessions
- Authentication
- JWT handling
- Password hashing
- Configuration
- Exception handling

This separation keeps individual route handlers focused on API operations rather than mixing validation, security, and database infrastructure together.

---

## Database Design

The application uses a relational database model.

Each major entity has its own **Primary Key (PK)**, while related entities are connected using **Foreign Keys (FKs)**.

### Core Entities

The backend currently manages six major entities:

| Entity | Description |
|---|---|
| `User` | Stores administrator credentials and authorization information |
| `Patient` | Stores patient information |
| `Doctor` | Stores doctor information |
| `Staff` | Stores hospital staff information |
| `Appointment` | Connects patients with doctors for scheduled appointments |
| `MedicalRecord` | Stores diagnosis and treatment information for patients |

---

## Primary Keys

The following fields uniquely identify records:

```text
patients.id
doctors.id
staff.id
users.id
appointments.id
medical_records.id
```

---

## Foreign Keys

Appointments connect patients and doctors:

```text
appointments.patient_id  →  patients.id
appointments.doctor_id   →  doctors.id
```

Medical records connect patients and doctors:

```text
medical_records.patient_id  →  patients.id
medical_records.doctor_id   →  doctors.id
```

This prevents unnecessary duplication of patient and doctor information.

For example, an appointment stores:

```text
patient_id = "P001"
doctor_id  = "D001"
```

instead of storing:

```text
patient_name
patient_phone
doctor_name
doctor_phone
```

The actual patient and doctor information remains in their respective tables.

---

## SQLAlchemy Relationships

Foreign keys define the database-level relationships, while SQLAlchemy's `relationship()` provides convenient object-level navigation between related models.

For example:

```python
patient = relationship(
    "Patient",
    back_populates="appointments"
)

doctor = relationship(
    "Doctor",
    back_populates="appointments"
)
```

This allows related objects to be accessed directly through an appointment:

```python
appointment.patient.name
appointment.patient.phone

appointment.doctor.name
appointment.doctor.phone
```

This approach allows related information to be returned through API response schemas without duplicating the same data inside the appointment or medical record tables.

---

## Authentication & Authorization

The API uses **JWT access tokens** for authentication.

Authentication is handled through FastAPI dependencies so that protected routes can consistently verify the current administrator and their permissions.

### Password Security

Passwords are never stored directly in the database.

They are hashed using **Bcrypt** before being stored.

```text
Plain Password
      ↓
    Bcrypt
      ↓
Password Hash
      ↓
  Database
```

---

## Administrative Roles

The system supports two administrative privilege levels.

### Primary Admin

The Primary Admin is created during the initial system setup.

The Primary Admin can:

- Manage hospital data
- Create other administrators
- View administrator accounts
- Delete normal administrators

The Primary Admin cannot be deleted through the API.

### Normal Admin

Normal administrators can manage:

- Patients
- Doctors
- Staff
- Appointments
- Medical Records

Normal administrators cannot create or delete administrator accounts.

---

## Protected Routes

Hospital management routes require an authenticated administrator.

Authentication and authorization are implemented using FastAPI dependencies.

The general authentication flow is:

```text
Client
  ↓
Login
  ↓
Authentication Endpoint
  ↓
JWT Access Token
  ↓
Protected API Request
  ↓
Authentication Dependency
  ↓
Verify Token
  ↓
Identify Administrator
  ↓
Check Permissions
  ↓
Execute Endpoint
```

Authenticated requests use the standard Bearer token format:

```http
Authorization: Bearer <access_token>
```

---

# API Endpoints

The API is organized into separate routers based on hospital functionality.

## Authentication

Handles administrator authentication and JWT token generation.

Typical operations include:

```text
POST /auth/login
```

---

## Patients

Manages patient records.

```text
POST   /patients
GET    /patients
GET    /patients/{patient_id}
PUT    /patients/{patient_id}
DELETE /patients/{patient_id}
```

---

## Doctors

Manages doctor information.

```text
POST   /doctors
GET    /doctors
GET    /doctors/{doctor_id}
PUT    /doctors/{doctor_id}
DELETE /doctors/{doctor_id}
```

---

## Staff

Manages hospital staff information.

```text
POST   /staff
GET    /staff
GET    /staff/{staff_id}
PUT    /staff/{staff_id}
DELETE /staff/{staff_id}
```

---

## Appointments

Appointments establish relationships between patients and doctors.

```text
POST   /appointments
GET    /appointments
GET    /appointments/{appointment_id}
PUT    /appointments/{appointment_id}
DELETE /appointments/{appointment_id}
```

Appointments reference patients and doctors using foreign keys rather than duplicating their information.

---

## Medical Records

Medical records connect patients with doctors and store medical information such as diagnosis and treatment.

```text
POST   /medical-records
GET    /medical-records
GET    /medical-records/{record_id}
PUT    /medical-records/{record_id}
DELETE /medical-records/{record_id}
```

---

## Request & Response Validation

Pydantic schemas are used to validate incoming request data and define API response structures.

The general request flow is:

```text
HTTP Request
     ↓
Pydantic Schema
     ↓
Validation
     ↓
Route Handler
     ↓
SQLAlchemy Model
     ↓
Database
```

Using separate schemas and models keeps database structure independent from the API's public request and response format.

---

## Exception Handling

The application uses centralized exception handling to provide consistent API error responses.

Handled cases include:

- Resource not found
- Invalid authentication
- Unauthorized access
- Invalid request data
- Database-related errors

Centralized exception handling avoids duplicating the same error-handling logic across multiple routers.

---

# Database Migrations

**Alembic** is used to manage database schema changes.

Instead of recreating the database whenever a SQLAlchemy model changes, migrations allow schema changes to be tracked and applied incrementally.

## Create a Migration

After modifying a SQLAlchemy model:

```bash
alembic revision --autogenerate -m "describe the change"
```

## Apply Migrations

```bash
alembic upgrade head
```

## Check Current Migration

```bash
alembic current
```

### Migration Workflow

```text
Modify SQLAlchemy Model
          ↓
Generate Migration
          ↓
Review Migration
          ↓
alembic upgrade head
          ↓
Updated Database Schema
```

---

# Technology Stack

## Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy

## Database & Migrations

- SQLite
- Alembic

## Security

- JWT
- Bcrypt
- Passlib
- python-jose

## Development & Documentation

- Uvicorn
- OpenAPI
- Swagger UI
- ReDoc

---

# Getting Started

## Prerequisites

Make sure the following are installed:

- Python 3.10+
- Git
- pip

---

## 1. Clone the Repository

```bash
git clone https://github.com/hasssssankhalid0001-eng/hospital-management-api.git

cd hospital-management-api
```

---

## 2. Create a Virtual Environment

### macOS / Linux

```bash
python3 -m venv myenv

source myenv/bin/activate
```

### Windows

```powershell
python -m venv myenv

myenv\Scripts\activate
```

---

## 3. Install Dependencies

If the repository contains `requirements.txt`:

```bash
pip install -r requirements.txt
```

Otherwise, install the required packages manually:

```bash
pip install fastapi uvicorn sqlalchemy alembic
pip install "python-jose[cryptography]"
pip install "passlib[bcrypt]"
pip install python-dotenv
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
APP_NAME=Hospital Management API
APP_VERSION=1.0.0
SECRET_KEY=your-secret-key
```

Use a strong randomly generated secret key for deployment.

Never commit `.env` files or production secrets to GitHub.

---

## 5. Apply Database Migrations

```bash
alembic upgrade head
```

This creates or updates the database schema according to the latest migration.

---

## 6. Create the Initial Administrator

```bash
python create_admin.py
```

The initial administrator becomes the Primary Admin.

---

## 7. Start the Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically generates documentation from the application's OpenAPI schema.

## Swagger UI

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows you to:

- Explore available endpoints
- View request and response schemas
- Authenticate using JWT
- Send API requests
- Inspect API responses

## ReDoc

```text
http://127.0.0.1:8000/redoc
```

ReDoc provides an alternative interface for exploring the generated OpenAPI specification.

---

# Project Structure

The project is organized into separate modules based on responsibility.

```text
hospital-management-api/
│
├── app/
│   ├── main.py
│   │
│   ├── router/
│   │   ├── auth.py
│   │   ├── patient.py
│   │   ├── doctor.py
│   │   ├── staff.py
│   │   ├── appointment.py
│   │   └── medical_record.py
│   │
│   ├── schema/
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── doctor.py
│   │   ├── staff.py
│   │   ├── appointment.py
│   │   └── medical_record.py
│   │
│   ├── model/
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── doctor.py
│   │   ├── staff.py
│   │   ├── appointment.py
│   │   └── medical_record.py
│   │
│   └── util/
│       ├── database.py
│       ├── auth.py
│       ├── security.py
│       ├── exceptions.py
│       └── config.py
│
├── alembic/
│   └── versions/
│
├── create_admin.py
├── alembic.ini
├── requirements.txt
├── .env
└── README.md
```

---

# Engineering Concepts Demonstrated

This project demonstrates practical backend engineering concepts including:

- REST API design
- HTTP methods and status codes
- FastAPI routing
- Dependency injection
- Pydantic validation
- SQLAlchemy ORM
- Primary keys and foreign keys
- Relational database modeling
- Database normalization
- SQLAlchemy relationships
- One-to-many relationships
- JWT authentication
- Password hashing
- Role-based authorization
- Protected routes
- Middleware
- Centralized exception handling
- Environment-based configuration
- Database migrations with Alembic
- OpenAPI documentation

---

# Roadmap

The core local-development backend is implemented.

### Planned

- [ ] PostgreSQL
- [ ] Docker containerization
- [ ] Production configuration
- [ ] Cloud deployment
- [ ] Production database configuration
- [ ] Automated testing
- [ ] API test suite
- [ ] Expanded API documentation
- [ ] Production-ready logging and monitoring
