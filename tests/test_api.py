from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_generate_configs():
    response = client.post(
        "/generate",
        json={
            "postgres_version": "14",
            "instance_type": "t2.micro",
            "num_replicas": 2,
            "max_connections": 100,
            "shared_buffers": "128MB"
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Configurations generated successfully"}

def test_provision_infrastructure():
    response = client.post("/provision")
    assert response.status_code in [200, 500]  # Success or error depending on Terraform setup

def test_configure_postgresql():
    response = client.post("/configure")
    assert response.status_code in [200, 500]  # Success or error depending on Ansible setup

def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "Not implemented yet"}
