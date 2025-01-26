# URL Shortener Service

A URL shortening service with a frontend in React and Vite, and a backend API in FastAPI using SQLite to manage shortened URLs. The project is set up with Docker and Docker Compose to simplify the deployment and environment management.

## Features

- **Frontend**: A web interface where you can enter a URL to shorten and view the 5 most recent shortened URLs.
- **API Backend**: FastAPI service to create, list, and redirect shortened URLs.
- **Pages**:
  - **Home**: Enter URLs to shorten and view the 5 most recent shortened URLs.
  - **History**: View all shortened URLs.

## Technologies Used

- **Frontend**: React, Vite
- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Docker**: Docker Compose to orchestrate services
- **Testing**: Pytest for backend testing

## Prerequisites

- A classic Linux environment
- docker
- docker-compose
- Make

## Installation

### 1. Clone the project

- git clone git@github.com:tgeorge42/URL_shortener.git
- cd URL_shortener

### 2. Build and run the project

Make sure you have make, docker and docker-compose installed.

Use the "make" command.

This will build and start the backend and frontend services in Docker containers.

The backend will be available at http://localhost:8000.
The frontend will be available at http://localhost:5173.

### 3. (Optional) Run backend tests

Use the "make test" command to run a few backend tests
