# Backend for Pipeline Management Application

This repository contains the backend services for the **Pipeline Management Application**, built with **FastAPI** and **PostgreSQL**, and deployed on **Render**. The backend is responsible for handling user authentication, data management, and backend logic like verifying Directed Acyclic Graphs (DAGs) and allowing authenticated users to download pipeline structures.

---

## Features

- **Authentication**:
  - Utilizes **OAuth2**, **JWT (JSON Web Tokens)** (via `python-jose`), and **Pydantic** for secure authentication.
  - User session management and token-based access control.

- **Database**:
  - **SQLAlchemy** ORM for seamless database interactions.
  - **PostgreSQL** deployed on **Render** for storing user data and pipeline information.

- **API Endpoints**:
  - Handle authentication (`register`, `login`).
  - Store and retrieve pipeline structures.
  - Verify if the pipeline is a DAG (Directed Acyclic Graph).
  - Allow authenticated users to download pipeline data.

- **Integration**:
  - Fully integrated with the [frontend application](https://github.com/Boss-Lord-Sean-Gangster/Pipeline-frontend) deployed on **Vercel**.

---

## Folder Structure
backend/ ├── auth.py # Handles user authentication and token generation ├── database.py # Manages database connection and initialization ├── models.py # Defines database models using SQLAlchemy ├── main.py # Contains API routes and application logic ├── requirements.txt # Lists all dependencies for the project


---

## Getting Started

### Prerequisites

- **Python 3.9+**
- **PostgreSQL**
- Dependencies listed in `requirements.txt`.

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-backend-repo.git
   cd backend

2. **Start the backend server**:

   ```bash
   uvicorn main:app --reload



