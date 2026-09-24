import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session,SQLModel,create_engine
from app.database import get_session
from app.enums import Role
from app.models import User
from app.security import hash_password
from main import app

TEST_DATABASE_URL=os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:devpassword@localhost:5432/bookstore_test",
)
test_engine=create_engine(TEST_DATABASE_URL,pool_pre_ping=True)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session]=get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

def make_user(session,username,role,password="Password123"):
    user=User(
        username=username,
        email=f"{username}@example.com",
        hashed_password=hash_password(password),
        role=role,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def headers_for(client,username,password="Password123"):
    challenge=client.get("/auth/challenge").json()
    answer=",".join(str(n) for n in sorted(challenge["numbers"]))
    response=client.post(
        "/auth/login",
        params={"challenge_token":challenge["challenge_token"],"challenge_answer":answer},
        data={"username":username,"password":password},
    )
    return {"Authorization":f"Bearer {response.json()['access_token']}"}

@pytest.fixture(name="customer")
def customer_fixture(session,client):
    make_user(session,"amina",Role.customer)
    return headers_for(client,"amina")

@pytest.fixture(name="staff")
def staff_fixture(session,client):
    make_user(session,"karim",Role.staff)
    return headers_for(client,"karim")

@pytest.fixture(name="admin")
def admin_fixture(session,client):
    make_user(session,"owner",Role.admin)
    return headers_for(client,"owner")

@pytest.fixture(name="a_book")
def a_book_fixture(client,staff):
    author=client.post("/authors",json={"name":"Frank Herbert"},headers=staff).json()
    fiction=client.post("/genres",json={"name":"fiction"},headers=staff).json()
    response=client.post(
        "/books",
        json={
            "title":"Dune",
            "author_id":author["id"],
            "genre_ids":[fiction["id"]],
            "price":12.5,
            "stock":3,
        },
        headers=staff,
    )
    return response.json()
