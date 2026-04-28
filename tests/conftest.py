import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.core.dependencies import get_db
from main import app

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL,
                       connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture()
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture()
def auth_headers(client):
    client.post("auth/register", json={
        "email": "test@email.com",
        "password": "123456"
    })

    response = client.post("auth/login", json={
        "email": "test@email.com",
        "password": "123456"
    })

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture()
def registered_vehicle(client, auth_headers):
    response = client.post("/vehicles/", json={
        "plate": "ABC1234",
        "type": "cavalo",
        "company_cnpj": "00000123456789"
    }, headers=auth_headers)

    return response.json()["data"]