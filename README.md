# Messenger Project - Phase 3 and 4

A private messenger application implemented in Python.

This project continues the previous messenger phases and migrates the application
from raw TCP socket communication to a REST API using FastAPI.

## Phase 3

Phase 3 focuses on building an HTTP API with FastAPI.

## Project Status

Phase 3 is currently under development.

The project currently supports:

* User registration with password validation
* Secure password hashing using Argon2
* JWT-based authentication
* User login using OAuth2 password flow
* Current-user identification using JWT
* Protected message endpoints
* Private messaging between registered users
* Conversation filtering between two users
* Custom application exceptions
* Thread-safe in-memory storage
* Structured logging
* Swagger API documentation

Automated tests will be added in the next development stage.

## Running the Application

Before running the application, configure the required environment variables.

### JWT Secret

Generate a secure JWT secret:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

On PowerShell:

```powershell
$env:MESSENGER_JWT_SECRET="your-generated-secret"
```

### Application Environment

For development:

```powershell
$env:MESSENGER_ENV="development"
```

For production:

```powershell
$env:MESSENGER_ENV="production"
```

### Start the API

Run the FastAPI application with Uvicorn:

```bash
uv run uvicorn src.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Authentication

The application uses JWT Bearer authentication.

Users first register with a username and password. Passwords are never stored in plain text and are hashed using Argon2.

After registration, users can log in and receive a JWT access token.

### Register

```http
POST /users
```

Example request:

```json
{
  "username": "maryam",
  "password": "Maryam123"
}
```

Example response:

```json
{
  "id": 1,
  "username": "maryam"
}
```

### Login

```http
POST /auth/token
```

The login endpoint accepts username and password using the OAuth2 password form.

A successful login returns:

```json
{
  "access_token": "<jwt-token>",
  "token_type": "bearer"
}
```

The returned token must be sent with protected requests:

```text
Authorization: Bearer <jwt-token>
```

When using Swagger UI, authentication can be performed using the **Authorize** button.

### Current User

```http
GET /auth/me
```

This endpoint returns information about the currently authenticated user.

Example response:

```json
{
  "id": 1,
  "username": "maryam"
}
```

## Messaging

Message endpoints require authentication.

The sender is determined automatically from the authenticated user's JWT token and cannot be provided manually by the client.

### Send a Message

```http
POST /messages
```

Example request:

```json
{
  "receiver": "ali",
  "content": "Hello Ali"
}
```

Example response:

```json
{
  "id": 1,
  "sender": "maryam",
  "receiver": "ali",
  "content": "Hello Ali"
}
```

Users cannot:

* Send messages without authentication
* Send messages to users that do not exist
* Send private messages to themselves
* Manually impersonate another sender

### Get Messages

```http
GET /messages
```

Returns messages associated with the currently authenticated user.

A user can only view conversations in which they are either the sender or receiver.

### Get a Conversation

To retrieve messages exchanged with a specific user:

```http
GET /messages?with_user=ali
```

This returns messages in both directions:

```text
maryam -> ali
ali -> maryam
```

## Validation

Pydantic is used for request validation.

Usernames:

* Must contain between 3 and 32 characters
* Must start with a letter
* May contain letters, numbers, and underscores

Passwords:

* Must contain between 8 and 128 characters

Messages:

* Cannot be empty
* Cannot exceed 2000 characters

## Error Handling

The application uses custom domain exceptions for common errors, including:

* Duplicate usernames
* Missing users
* Attempts to send messages to oneself

The API converts these errors into appropriate HTTP responses such as:

```text
400 Bad Request
401 Unauthorized
404 Not Found
409 Conflict
422 Unprocessable Entity
```

## Logging

The application supports separate development and production logging environments.

Logs are written to the `logs/` directory using a rotating file handler.

The logging system supports:

* Structured JSON file logs
* Console logs in development mode
* Log rotation
* Multiple log levels
* Separate module loggers

Sensitive information is not intentionally written to logs, including:

* Plain-text passwords
* Password hashes
* JWT access tokens
* JWT secrets
* Private message contents

## In-Memory Storage

Users and messages are currently stored in memory.

The shared storage is protected using thread locks to support concurrent requests safely.

Because storage is in memory, all registered users and messages are removed when the application restarts.

Persistent database storage can be introduced in a later phase.

## Development Tools

Run Ruff lint checks:

```bash
uv run ruff check .
```

Automatically fix supported lint issues:

```bash
uv run ruff check . --fix
```

Format the project:

```bash
uv run ruff format .
```

Run all pre-commit hooks:

```bash
uv run pre-commit run --all-files
```

Install the Git pre-commit hook:

```bash
uv run pre-commit install
```

## Testing

The project uses pytest for automated testing.

Tests will cover areas such as:

* User registration
* Username validation
* Duplicate users
* Password authentication
* Invalid login attempts
* JWT authentication
* Protected endpoints
* Message creation
* Messaging nonexistent users
* Self-messaging prevention
* Conversation filtering

Run the test suite with:

```bash
uv run pytest
```

## Phase 3 Architecture

The current application follows a layered structure:

```text
Client / Swagger / Postman
            |
            v
         FastAPI
            |
            v
          Routers
            |
            v
         Services
            |
            v
    In-Memory Storage
```

Authentication follows this flow:

```text
Username + Password
        |
        v
 Password Verification
        |
        v
      JWT Token
        |
        v
Authorization: Bearer <token>
        |
        v
 Current User Resolution
        |
        v
 Protected API Endpoint
```
