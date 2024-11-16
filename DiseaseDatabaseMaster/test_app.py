import pytest
from DiseaseDatabaseMaster.cozom_web_based_app import app  # Importing from the correct folder path

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Cozom Health Assessment Web Application" in response.data

def test_get_database(client):
    response = client.get('/database')
    assert response.status_code == 200 or response.status_code == 404  # Depends if data is available


