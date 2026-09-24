from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.database import create_db_and_tables
from app.routers import auth,authors,books,genres,orders,users

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield

app=FastAPI(
    title=settings.app_name,
    description="Book Store API with authentication, roles, PostgreSQL relationships and tests",
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(authors.router)
app.include_router(genres.router)
app.include_router(books.router)
app.include_router(orders.router)

@app.get("/",tags=["system"])
def read_root():
    return {"message":f"Welcome to {settings.app_name}"}
