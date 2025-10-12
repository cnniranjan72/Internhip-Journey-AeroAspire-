import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def get_token(client):
    res = client.post('/api/v1/auth/login', json={
        "username": "niranjan-admin",
        "password": "pass123"
    })
    return res.json["access_token"]

def test_root(client):
    res = client.get('/api/v1/')
    assert res.status_code == 200
    assert b"API" in res.data

def test_login_success(client):
    res = client.post('/api/v1/auth/login', json={
        "username": "Niranjan-Admin",
        "password": "pass123"
    })
    assert res.status_code == 200
    assert "access_token" in res.json

def test_login_failure(client):
    res = client.post('/api/v1/auth/login', json={
        "username": "wrong",
        "password": "invalid"
    })
    assert res.status_code == 401

def test_create_task(client):
    token = get_token(client)
    res = client.post('/api/v1/tasks', json={"title": "Test Task"}, headers={
        "Authorization": f"Bearer {token}"
    })
    assert res.status_code == 201
    assert res.json["title"] == "Test Task"

def test_get_tasks(client):
    res = client.get('/api/v1/tasks')
    assert res.status_code == 200
    assert isinstance(res.json, list)

def test_update_task(client):
    token = get_token(client)
    client.post('/api/v1/tasks', json={"title": "Update Task"}, headers={
        "Authorization": f"Bearer {token}"
    })
    res = client.put('/api/v1/tasks/1', json={"completed": True}, headers={
        "Authorization": f"Bearer {token}"
    })
    assert res.status_code == 200
    assert res.json["completed"] == True

def test_delete_task(client):
    token = get_token(client)
    client.post('/api/v1/tasks', json={"title": "Delete Task"}, headers={
        "Authorization": f"Bearer {token}"
    })
    res = client.delete('/api/v1/tasks/1', headers={
        "Authorization": f"Bearer {token}"
    })
    assert res.status_code == 200
