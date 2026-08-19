# Messenger Project - Phase 3 and 4

A private messenger application implemented in Python.

This project continues the previous messenger phases and migrates the application
from raw TCP socket communication to a REST API using FastAPI.

## Phase 3

Phase 3 focuses on building an HTTP API with FastAPI.

### Current Features

- FastAPI application structure
- User router
- Message router
- In-memory user and message storage
- Pydantic request and response models
- Structured application logging
- Development and production logging environments
- JWT configuration

### In Progress

- Password hashing
- JWT authentication
- Login endpoint
- Protected message endpoints
- Current-user authentication
- Conversation filtering
- Custom application exceptions
- Thread-safe in-memory storage
- Automated tests

## Tech Stack

- Python 3.12
- FastAPI
- Pydantic
- Uvicorn
- PyJWT
- pwdlib / Argon2
- uv
- Ruff
- pytest
- pre-commit

## Installation

Install project dependencies:

# Messenger Project - Phase 3 and 4

A private messenger application implemented in Python.

This project continues the previous messenger phases and migrates the application
from raw TCP socket communication to a REST API using FastAPI.

## Phase 3

Phase 3 focuses on building an HTTP API with FastAPI.

### Current Features

- FastAPI application structure
- User router
- Message router
- In-memory user and message storage
- Pydantic request and response models
- Structured application logging
- Development and production logging environments
- JWT configuration

### In Progress

- Password hashing
- JWT authentication
- Login endpoint
- Protected message endpoints
- Current-user authentication
- Conversation filtering
- Custom application exceptions
- Thread-safe in-memory storage
- Automated tests

## Tech Stack

- Python 3.12
- FastAPI
- Pydantic
- Uvicorn
- PyJWT
- pwdlib / Argon2
- uv
- Ruff
- pytest
- pre-commit

## Installation

Install project dependencies:

uv sync


‍Development Tools

Check the code with Ruff:

uv run ruff check .

Format the code:

uv run ruff format .

Run all pre-commit hooks:

uv run pre-commit run --all-files
API Documentation

FastAPI automatically provides interactive API documentation at:

http://127.0.0.1:8000/docs
Project Status
