🏥 Hospital Management API

A backend REST API for managing hospital operations, built with FastAPI and SQLAlchemy.

The Hospital Management API provides a secure administrative backend for managing patients, doctors, staff, appointments, and medical records.

The project focuses on REST API design, relational database modeling, authentication, authorization, database migrations, and clean backend architecture.

🚧 Project Status: Core backend functionality is complete. PostgreSQL, Docker, and deployment are the next development stages.

⸻

✨ Highlights

* RESTful API built with FastAPI
* SQLAlchemy ORM for database interaction
* Relational database design using primary and foreign keys
* JWT-based authentication
* Bcrypt password hashing
* Role-based authorization
* Primary Admin / Normal Admin privilege system
* Protected API routes
* Pydantic request validation
* SQLAlchemy model relationships
* Alembic database migrations
* Centralized exception handling
* Interactive API documentation with Swagger UI

⸻

🏗️ Architecture

The application follows a layered backend structure:

Routers → Schemas → Models → Database

Routers

Handle HTTP requests and API endpoints.

Examples:

* Patient routes
* Doctor routes
* Staff routes
* Appointment routes
* Medical record routes
* Authentication routes

Schemas

Pydantic models are responsible for:

* Request validation
* Response structure
* Controlling the data exposed through the API

Models

SQLAlchemy models represent the database entities and their relationships.

Utilities

Authentication, JWT handling, password hashing, database sessions, configuration, and exception handling are separated into utility modules.

This keeps API logic, validation, database logic, and security concerns separated rather than putting everything inside the route handlers.

⸻

🗄️ Database Design

The application uses a relational database model.

Each major entity has its own Primary Key (PK).

Related entities are connected using Foreign Keys (FK).

Primary Keys

The following fields uniquely identify records:

patients.id
doctors.id
staff.id
users.id
appointments.id
medical_records.id

Foreign Keys

Appointments connect patients and doctors:

appointments.patient_id  →  patients.id
appointments.doctor_id   →  doctors.id

Medical records connect patients and doctors:

medical_records.patient_id  →  patients.id
medical_records.doctor_id   →  doctors.id

This avoids storing duplicate patient or doctor information inside appointments and medical records.

For example, an appointment stores:

patient_id = "P001"
doctor_id  = "D001"

rather than storing:

patient_name
patient_phone
doctor_name
doctor_phone

The actual patient and doctor information remains in their respective tables.

SQLAlchemy Relationships

Foreign keys define the database-level relationship, while SQLAlchemy relationship() provides convenient object-level navigation.

For example:

patient = relationship("Patient", back_populates="appointments")
doctor = relationship("Doctor", back_populates="appointments")

This allows related patient and doctor objects to be accessed through an appointment.

⸻

🔐 Authentication & Authorization

The API uses JWT access tokens for authentication.

Passwords are never stored directly. They are hashed using Bcrypt before being stored in the database.

The system has two administrative privilege levels.

Primary Admin

The Primary Admin is created during the initial system setup.

The Primary Admin can:

* Manage hospital data
* Create other administrators
* View administrator accounts
* Delete normal administrators

The Primary Admin cannot be deleted through the API.

Normal Admin

Normal administrators can manage:

* Patients
* Doctors
* Staff
* Appointments
* Medical records

Normal administrators cannot create or delete administrator accounts.

Protected Routes

Hospital management routes require an authenticated administrator.

Authentication is handled through FastAPI dependencies, allowing authorization rules to be applied consistently across protected routes.

⸻

🧬 Core Entities

The backend currently manages six major entities:

User

Stores administrator credentials and authorization information.

Patient

Stores patient information such as name, contact details, age, gender, height, and weight.

Doctor

Stores doctor information including specialization, department, experience, and contact details.

Staff

Stores hospital staff information and department/role details.

Appointment

Connects a patient with a doctor for a scheduled appointment.

Medical Record

Connects a patient with a doctor and stores diagnosis and treatment information.

⸻

🛠️ Technology Stack

Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy

Database & Migrations

* SQLite for local development
* Alembic

Security

* JWT
* Passlib
* Bcrypt
* python-jose

Development

* Uvicorn
* Swagger / OpenAPI

⸻

🚀 Getting Started

1. Clone the repository

git clone https://github.com/hasssssankhalid0001-eng/hospital-management-api.git
cd hospital-management-api

2. Create a virtual environment

python -m venv myenv
source myenv/bin/activate

3. Install dependencies

pip install fastapi uvicorn sqlalchemy alembic python-jose[cryptography] passlib[bcrypt] python-dotenv

4. Configure environment variables

Create a .env file in the project root:

APP_NAME=Hospital Management API
APP_VERSION=1.0.0
SECRET_KEY=your-secret-key

Never commit .env or production secrets to GitHub.

5. Apply database migrations

alembic upgrade head

6. Create the initial administrator

python create_admin.py

7. Start the development server

uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000

Interactive Swagger documentation:

http://127.0.0.1:8000/docs

⸻

🔄 Database Migrations

Alembic is used to track and apply database schema changes.

After modifying a SQLAlchemy model:

alembic revision --autogenerate -m "describe the change"

Apply the migration:

alembic upgrade head

Check the current migration:

alembic current

This allows the database schema to evolve without manually recreating the database.

⸻

📚 API Documentation

FastAPI automatically generates OpenAPI documentation.

Once the server is running, the API can be explored and tested through:

Swagger UI

http://127.0.0.1:8000/docs

ReDoc

http://127.0.0.1:8000/redoc

⸻

🧠 Engineering Concepts Demonstrated

This project was built to practice and demonstrate practical backend engineering concepts including:

* REST API design
* HTTP methods and status codes
* Request and response validation
* Dependency injection with FastAPI
* SQLAlchemy ORM
* Primary keys and foreign keys
* One-to-many relationships
* Database normalization
* JWT authentication
* Password hashing
* Authorization and access control
* Middleware
* Exception handling
* Database migrations with Alembic
* Environment-based configuration

⸻

🗺️ Roadmap

The core local-development backend is implemented.

Upcoming work:

* Move from SQLite to PostgreSQL
* Dockerize the application
* Production configuration
* Deploy the API to the cloud
* Production testing
* Finalize API documentation

⸻

⚠️ Disclaimer

This project is built for learning and portfolio purposes.

It is not intended for use with real patient information or production healthcare environments.

⸻

👨‍💻 Author

Mohammad Hassan Khalid

B.Tech Electrical and Computer Engineering
Jamia Millia Islamia, New Delhi

GitHub: @hasssssankhalid0001-eng
