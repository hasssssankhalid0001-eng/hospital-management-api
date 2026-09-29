HOSPITAL MANAGEMENT API

A backend API for managing hospital operations, built with FastAPI and SQLAlchemy.

The project provides authenticated administrative access to manage patients, doctors, staff, appointments, and medical records. It also includes JWT-based authentication and separate privileges for the main administrator and normal administrators.

Project status: 🚧 In active development
Core API functionality, authentication, authorization, database models, and migrations are currently implemented. PostgreSQL, Docker, and deployment are planned next.

Features

Authentication & Authorization

* JWT-based authentication
* Secure password hashing using bcrypt
* Protected hospital management endpoints
* Main administrator and normal administrator privileges
* Main administrator can create and delete normal administrators
* Normal administrators can manage hospital data but cannot manage administrator accounts

Hospital Management

* Patient management
* Doctor management
* Staff management
* Appointment management
* Medical record management
* Relationships between patients, doctors, appointments, and medical records

Database

* SQLAlchemy ORM
* SQLite for local development
* Alembic for database migrations
* Relational database design with foreign keys and relationships

Tech Stack

Technology	Purpose
Python	Backend programming
FastAPI	REST API framework
Pydantic	Request and response validation
SQLAlchemy	ORM and database interaction
Alembic	Database migrations
SQLite	Local development database
JWT	Authentication
Passlib + bcrypt	Password hashing

Project Structure

hospital-management-api/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   ├── model/
│   │   ├── appointment.py
│   │   ├── doctor.py
│   │   ├── medical_record.py
│   │   ├── patient.py
│   │   ├── staff.py
│   │   └── user.py
│   │
│   ├── router/
│   │   ├── appointment.py
│   │   ├── auth.py
│   │   ├── doctor.py
│   │   ├── medical_record.py
│   │   ├── patient.py
│   │   └── staff.py
│   │
│   ├── schema/
│   │   ├── appointment.py
│   │   ├── doctor.py
│   │   ├── medical_record.py
│   │   ├── patient.py
│   │   ├── staff.py
│   │   └── user.py
│   │
│   ├── util/
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   └── security.py
│   │
│   └── main.py
│
├── create_admin.py
├── make_primary_admin.py
├── alembic.ini
├── .gitignore
└── README.md

Authentication Flow

The API uses JWT access tokens for authenticated requests.

Client
  │
  │ username + password
  ▼
POST /auth/login
  │
  ▼
Password verification
  │
  ▼
JWT access token
  │
  ▼
Protected API endpoints

Protected endpoints require:

Authorization: Bearer <access_token>

Admin Privileges

The project currently has two levels of administrative access.

Main Administrator

The primary administrator can:

* Manage hospital data
* Create normal administrators
* View administrator accounts
* Delete normal administrators

The main administrator cannot be deleted through the API.

Normal Administrator

Normal administrators can:

* Manage patients
* Manage doctors
* Manage staff
* Manage appointments
* Manage medical records

They cannot:

* Create administrators
* Delete administrators
* Modify the primary administrator

Running Locally

1. Clone the repository

git clone https://github.com/hasssssankhalid0001-eng/hospital-management-api.git
cd hospital-management-api

2. Create a virtual environment

python -m venv myenv

Activate it:

macOS/Linux

source myenv/bin/activate

3. Install dependencies

pip install fastapi uvicorn sqlalchemy alembic python-jose[cryptography] passlib[bcrypt] python-dotenv

4. Configure environment variables

Create a .env file in the project root:

APP_NAME=Hospital Management API
APP_VERSION=1.0.0
SECRET_KEY=your-secret-key

Do not commit .env to GitHub.

5. Apply database migrations

alembic upgrade head

6. Create the initial administrator

python create_admin.py

The administrator can then log in through:

POST /auth/login

7. Start the server

uvicorn app.main:app --reload

The interactive API documentation is available at:

http://127.0.0.1:8000/docs

Database Migrations

Alembic is used to manage database schema changes.

Create a migration after modifying the SQLAlchemy models:

alembic revision --autogenerate -m "description of change"

Apply migrations:

alembic upgrade head

API Areas

Area	Endpoint Prefix
Authentication	/auth
Patients	/patients
Doctors	/doctors
Staff	/staff
Appointments	/appointments
Medical Records	/medical-records

Most hospital-management endpoints require administrator authentication.

Current Development Roadmap

* FastAPI application structure
* SQLAlchemy models
* CRUD operations
* Relational models and foreign keys
* Alembic migrations
* JWT authentication
* Password hashing
* Admin authorization
* Main-admin / normal-admin privileges
* PostgreSQL database
* Docker containerization
* Cloud deployment
* Production configuration
* Final API testing and documentation
