Hospital Management API

A backend REST API for managing hospital operations, built with FastAPI, SQLAlchemy, and Alembic.

The system provides authenticated administrative access to manage patients, doctors, staff, appointments, and medical records. It also implements JWT-based authentication with separate privileges for the primary administrator and normal administrators.

🚧 Status: In active development
Core backend functionality and authentication are implemented. PostgreSQL, Docker, and deployment are planned next.

Features

* RESTful API built with FastAPI
* SQLAlchemy ORM for database operations
* Alembic database migrations
* JWT-based authentication
* Bcrypt password hashing
* Protected API routes
* Primary-admin and normal-admin authorization
* Patient management
* Doctor management
* Staff management
* Appointment management
* Medical record management
* Foreign-key relationships between related entities
* Request and response validation with Pydantic
* Centralized exception handling

Authentication & Authorization

The application uses JWT access tokens to protect administrative endpoints.

There are two levels of administrative access:

Primary Administrator

The primary administrator is created during initial setup and can:

* Manage hospital data
* Create administrators
* View administrator accounts
* Delete normal administrators

The primary administrator cannot be deleted through the API.

Normal Administrator

Normal administrators can manage hospital data, including:

* Patients
* Doctors
* Staff
* Appointments
* Medical records

Normal administrators cannot create or delete administrator accounts.

Database Design

The application uses a relational database with foreign keys and SQLAlchemy relationships.

The main entities include:

* Patient
* Doctor
* Staff
* Appointment
* Medical Record
* User

Appointments and medical records reference patients and doctors through foreign keys rather than duplicating their information.

Project Architecture

The application follows a layered structure:

app/
├── model/       # SQLAlchemy database models
├── schema/      # Pydantic request/response schemas
├── router/      # API endpoints
├── util/        # Database, authentication and security utilities
└── main.py      # FastAPI application entry point

This separation keeps database models, validation, API routes, and supporting functionality organized as the project grows.

Technology Stack

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* Alembic
* SQLite — local development
* JWT
* Passlib / Bcrypt

Running Locally

Clone the Repository

git clone https://github.com/hasssssankhalid0001-eng/hospital-management-api.git
cd hospital-management-api

Create a Virtual Environment

python -m venv myenv
source myenv/bin/activate

Install Dependencies

pip install fastapi uvicorn sqlalchemy alembic python-jose[cryptography] passlib[bcrypt] python-dotenv

Configure Environment Variables

Create a .env file in the project root:

APP_NAME=Hospital Management API
APP_VERSION=1.0.0
SECRET_KEY=your-secret-key

Do not commit .env to the repository.

Apply Database Migrations

alembic upgrade head

Create the Initial Administrator

python create_admin.py

Start the Server

uvicorn app.main:app --reload

Interactive API documentation is available at:

http://127.0.0.1:8000/docs

Database Migrations

Database schema changes are managed using Alembic.

Create a migration after modifying the SQLAlchemy models:

alembic revision --autogenerate -m "description of change"

Apply migrations:

alembic upgrade head

Project Roadmap

* FastAPI backend architecture
* SQLAlchemy database models
* CRUD operations
* Entity relationships
* Alembic migrations
* JWT authentication
* Password hashing
* Admin authorization
* Primary-admin privileges
* PostgreSQL
* Docker
* Cloud deployment
* Production configuration
* Final testing and documentation
