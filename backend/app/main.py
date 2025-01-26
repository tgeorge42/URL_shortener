# /app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import shortlinks
from app.database.database import Base, engine

app = FastAPI()

# Middleware for CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Include the routes from the shortlinks router
app.include_router(shortlinks.router, prefix="/api")

# Home route
@app.get("/")
def read_root():
    return {
        "message": "Welcome to FastAPI with SQLite!",
        "description": "This API allows you to shorten URLs and retrieve original URLs using short codes.",
        "version": "1.0.0",
        "available_routes": {
            "/api/shorten/": "Create a short URL",
            "/api/urls/{short_code}/": "Retrieve the original URL for a given short code",
            "/api/list/": "Get the list of all shortened URLs",
        },
    }
