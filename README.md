# Goodreads API - Local Setup & Testing

This project runs a FastAPI-based Goodreads-like API locally using Docker Compose. It includes pre-seeded data so that endpoints in Swagger UI (/docs) show ready content.

---

## Requirements

- Docker
- Docker Compose

---

## Setup & Run

1. Clone the repository:

   ```bash
   git clone https://github.com/black-x98/goodreads
   cd goodreads

Build and start the containers:

    docker compose up --build

This will:

    Build the api container

    Start a PostgreSQL database container (db)

    Automatically run database migrations and seed initial data

Wait until the API logs show:

    INFO: Waiting for application startup.

    This means the API is ready.

Accessing the API

Open your browser and go to:

http://127.0.0.1:8000/docs

This is the FastAPI Swagger UI where you can:

    View all endpoints

    Test requests interactively

    See seeded users, books, reviews, and followers

Seed Data

On startup, the API automatically inserts seed data if it doesn't already exist. The seed includes:

    Users (e.g., Alice, Bob)

    Books (e.g., Clean Code, The Pragmatic Programmer)

    Reviews for books

    Follower relationships between users

Note: The seeding is fully idempotent. Restarting the container will not create duplicates.
Notes

    The API uses environment variables for DB connection. Defaults are:

DB_HOST=db
DB_PORT=5432
DB_NAME=goodreads
DB_USER=postgres
DB_PASSWORD=postgres

To stop the containers:

docker compose down

To persist DB data between runs, the project uses a Docker volume postgres_data.