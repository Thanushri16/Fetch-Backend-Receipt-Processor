"""Module test_app for testing the functionalities of the app 
implementing the Receipt Processor web service."""

import pytest
import json
from app import app

@pytest.fixture()
def client():
    return app.test_client()

def test_process_receipts_1(client):
    """Function that tests the process_receipts method"""
    with open('example_receipt1.json', 'r') as file:
        data = json.load(file)
    response = client.post('/receipts/process', json=data)
    assert response.status_code == 200
    assert 'id' in response.json

def test_process_receipts_2(client):
    """Function that tests the process_receipts method"""
    with open('example_receipt1.json', 'r') as file:
        data = json.load(file)
    response = client.post('/receipts/process', data=data)
    assert response.status_code == 400
    assert 'id' not in response.json

def test_get_points_1(client):
    """Function that tests the get_points method"""
    with open('example_receipt1.json', 'r') as file:
        data = json.load(file)
    response_post = client.post('/receipts/process', json=data)
    id = response_post.json["id"]
    response_get = client.get(f'/receipts/{id}/points')
    assert response_get.status_code == 200
    assert 'points' in response_get.json
    assert response_get.json["points"] == 28

def test_get_points_2(client):
    """Function that tests the get_points method"""
    id = "1"
    response_get = client.get(f'/receipts/{id}/points')
    assert response_get.status_code == 404
    assert 'points' not in response_get.json

def test_get_receipts(client):
    """Function that tests the get_receipts method"""
    with open('example_receipt1.json', 'r') as file:
        data = json.load(file)
    client.post('/receipts/process', data=data)
    response2 = client.get('/receipts')
    assert response2.status_code == 200

def test_get_receipt(client):
    """Function that tests the get_receipt method"""
    with open('example_receipt2.json', 'r') as file:
        data = json.load(file)
    response_post = client.post('/receipts/process', json=data)
    id = response_post.json["id"]
    response_get = client.get(f'/receipts/{id}')
    assert response_get.status_code == 200
    assert 'Receipt' in response_get.json
    assert response_get.json["Receipt"]["id"] == id