# User Manager FastAPI

User Manager FastAPI is a simple user management API built using FastAPI.
It provides basic CRUD (Create, Read, Update, Delete) operations for users.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [API Endpoints](#api-endpoints)
- [Testing with SwaggerUI](#testing-the-api-with-swagger-ui)
- [Project author](#project-author)

## Features

- CRUD operations for users (Create, Read, Update, Delete).
- Info endpoint
  - Function that counts the number of users registered in the last 7 days.
  - Function that returns the top 5 users with the longest names.
  - Function that determines what proportion of users have an email address registered in a particular domain
- Simple and straightforward project structure.

## Project Structure

The project follows the following directory structure:

```text
Quazar_fastapi_test_task/
├── alembic/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   ├── schemas/
│   ├── core/
│   ├── db/
│   ├── repositories/
│   ├── services/
│   ├── utils/
├── .env
├── .gitignore
├── alembic.ini
├── README.md
├── main.py
├── requirements.txt
```

- `alembic`: Database migration files (if used).
- `app`: Contains the main application code.
  - `api`: Contains API endpoints for tasks and users.
    - `endpoints`: Task and user API endpoints.
    - `schemas`: Pydantic models for request and response.
  - `core`: Core constants and configurations.
  - `db`: Database configuration and models.
  - `repositories`: Pattern Repository. Working with the database through a separate layer.
  - `services`: Service approach. Removes business logic from routes than increases the level of abstraction and independence.
  - `utils`: Pattern Unit Of Work. Working with the database through its asynchronous context manager.
- `.env`: Store environment variables (e.g., database credentials).
- `.gitignore`: Lists files and directories to be ignored by version control.
- `alembic.ini`: Alembic configuration (if used).
- `README.md`: Documentation about the project.
- `requirements.txt`: List of project dependencies.

## Getting Started

### Prerequisites

Before running the application, make sure you have the following prerequisites installed:

Python 3.11

Fastapi 0.109.2

Asyncpg 0.29.0

Psycopg 3.1.18

Alembic 1.13.1

SQLAlchemy 2.0.25

Uvicorn 0.27.1

PostgreSQL 15

### Installation

1. PostgreSQL database servers (version 15 and higher) are required for the project to work correctly,
you can install it at the link: <https://www.postgresql.org/>

2. Create a PostgreSQL database

3. Clone the repository:

```bash
git clone git@github.com:iliya12321/Quazar_fastapi_test_task.git
```

4. Create a virtual environment (recomended):

```bash
py -3.11 -m venv venv (Windows)
python3 -m venv venv (Linux, MacOS)

source venv/Scripts/activate (Windows)
source venv/bin/activate (Linux, MacOS)
```

5. Update pip in the virtual environment:

```bash
python -m pip install --upgrade pip
```

6. Install project dependencies:

```bash
pip install -r requirements.txt
```

7. Copy the .env_sample file and rename it to .env. The .env file should be on the same level as main.py. Set the parameter values in the file:

```text
DB_HOST=<db host>
DB_PORT=<db port>
DB_USER=<postgres user>
DB_PASS=<postgres password>
DB_NAME=<db name>
```

## Usage

### Running the Application

To run the FastAPI application locally, use the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Replace `0.0.0.0` and `8000` with your desired host and port.

Or you can just run `main.py`:

```bash
python main.py
```

### API Endpoints

The API exposes the following endpoints:

- `GET /api/v1/users/info`: [Features](#features) Info edpoint
- `GET /api/v1/users/`: Retrieve a list of users with pagination.
- `POST /api/v1/users/`: Create a new user.
- `GET /api/v1/users/{user_id}`: Retrieve a specific user.
- `PUT /api/v1/users/{user_id}`: Update a specific user.
- `DELETE /api/v1/users/{user_id}`: Delete a specific user.

## Testing the API with Swagger UI

Fast API comes with Swagger UI. This tool is automatically generated based on your API's route definitions and Pydantic models.

### Accessing Swagger UI

Once the API is running, Swagger UI can be accessed on the following URL:

```bash
http://127.0.0.1:8000/docs
```

You can use swagger UI to:

1. **Browse Endpoints**
2. **Send Requests**
3. **View Responses**
4. **Test Validations**

## To Test with SwaggerUI, you can do the following for each endpoint explained above

1. Open your web browser and navigate to the /docs path as mentioned above.

2. Explore the available endpoints and select the one you want to test.

3. Click on the "Try it out" button to open an interactive form where you can input data.

4. Fill in the required parameters and request body (if applicable) according to the API documentation given above.

5. Click the "Execute" button to send the request to the API.

6. The response will be displayed below, showing the status code and response data.

7. You can also view example request and response payloads, which can be helpful for understanding the expected data format.

## Project author

[Iliya](https://github.com/iliya12321)
