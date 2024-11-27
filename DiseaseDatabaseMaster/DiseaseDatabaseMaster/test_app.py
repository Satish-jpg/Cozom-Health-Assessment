import pytest
from DiseaseDatabaseMaster.cozom_web_based_app import app  # Ensure the import path is correct

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
    assert response.status_code in [200, 404]  # Depends on implementation

def test_symptom_checker(client):
    response = client.get('/symptom-checker')
    assert response.status_code == 200
    assert b"Symptom Checker" in response.data  # Replace with actual content

def test_diagnosis(client):
    response = client.get('/diagnosis')
    assert response.status_code == 200
    assert b"Diagnosis Page" in response.data  # Replace with actual content

def test_body_part_valid(client):
    response = client.get('/body-part/1')  # Replace 1 with a valid part ID
    assert response.status_code == 200

def test_body_part_invalid(client):
    response = client.get('/body-part/99999')  # Replace 99999 with an invalid part ID
    assert response.status_code == 404

def test_invalid_route(client):
    response = client.get('/invalid-route')
    assert response.status_code == 404
