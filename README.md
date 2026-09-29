Hospital Management API

A RESTful backend API for managing hospital operations, built with FastAPI, SQLAlchemy, and Alembic.

The API provides authenticated administrative access for managing patients, doctors, staff, appointments, and medical records.

Status: In active development
Core backend functionality, database relationships, migrations, authentication, and authorization are implemented. PostgreSQL, Docker, and deployment are planned next.

Features

* Patient management
* Doctor management
* Staff management
* Appointment management
* Medical record management
* SQLAlchemy ORM
* Relational database design
* Primary key and foreign key relationships
* Alembic database migrations
* JWT authentication
* Bcrypt password hashing
* Protected API routes
* Primary admin and normal admin authorization
* Pydantic validation
* Centralized exception handling

Database Design

The application follows a relational database design using SQLAlchemy.

Each entity has its own primary key (PK) that uniquely identifies a record.

Relationships between entities are created using foreign keys (FKs).

Primary Keys

* Patient.id uniquely identifies a patient.
* Doctor.id uniquely identifies a doctor.
* Staff.id uniquely identifies a staff member.
* User.id uniquely identifies an administrator.
* Appointment.id uniquely identifies an appointment.
* MedicalRecord.id uniquely identifies a medical record.

Foreign Keys

Appointments and medical records connect existing entities using foreign keys instead of duplicating their information.

Appointment

* patient_id → patients.id
* doctor_id → doctors.id

This connects an appointment to one patient and one doctor.

MedicalRecord

* patient_id → patients.id
* doctor_id → doctors.id

This connects a medical record to the patient and doctor associated with it.

SQLAlchemy relationships are used on top of these foreign keys to navigate between related objects.


The database therefore stores relationships through PK/FK references, while SQLAlchemy provides convenient access to those related objects in the application.

Authentication

The API uses JWT access tokens for authentication.

There are two administrative privilege levels.

Primary Admin

The primary administrator is created during initial setup.

They can:

* Manage hospital data
* Create administrators
* View administrator accounts
* Delete normal administrators

The primary administrator cannot be deleted through the API.

Normal Admin

Normal administrators can manage hospital data, including:

* Patients
* Doctors
* Staff
* Appointments
* Medical records

They cannot create or delete administrator accounts.

Project Structure

The application is organized into separate layers:

* app/model — SQLAlchemy database models
* app/schema — Pydantic schemas
* app/router — API routes
* app/util — database, authentication, security, and utility modules
* app/main.py — FastAPI application entry point
* alembic/ — database migrations
* create_admin.py — initial administrator setup
* make_primary_admin.py — primary administrator setup

Tech Stack

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* Alembic
* SQLite
* JWT
* Passlib
* Bcrypt

Getting Started

Clone the repository

git clone https://github.com/hasssssankhalid0001-eng/hospital-management-api.git
cd hospital-management-api

Create a virtual environment

python -m venv myenv
source myenv/bin/activate

Install dependencies

pip install fastapi uvicorn sqlalchemy alembic python-jose[cryptography] passlib[bcrypt] python-dotenv

Configure environment variables

Create a .env file in the project root:

APP_NAME=Hospital Management API
APP_VERSION=1.0.0
SECRET_KEY=your-secret-key

Do not commit .env or any secrets to the repository.

Apply database migrations

alembic upgrade head

Create the initial administrator

python create_admin.py

Start the server

uvicorn app.main:app --reload

The interactive API documentation will be available at:

http://127.0.0.1:8000/docs

Database Migrations

Create a migration after changing the SQLAlchemy models:

alembic revision --autogenerate -m "description of change"

Apply migrations:

alembic upgrade head

Roadmap

* PostgreSQL database
* Docker containerization
* Cloud deployment
* Production configuration
* Final testing and documentation
