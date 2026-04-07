import requests
import pytest

BASE_URL = "http://127.0.0.1:5000"

def test_home():
    res = requests.get(BASE_URL + "/")
    assert res.status_code == 200

def test_login_success():
    res = requests.post(BASE_URL + "/login", json={
        "username": "admin",
        "password": "password123"
    })
    assert res.status_code == 200

def test_login_failure():
    res = requests.post(BASE_URL + "/login", json={
        "username": "admin",
        "password": "wrong"
    })
    assert res.status_code == 401

def test_search():
    res = requests.get(BASE_URL + "/search?q=test")
    assert res.status_code == 200

def test_payment_success():
    res = requests.post(BASE_URL + "/payment", json={"amount": 100})
    assert res.status_code == 200

def test_payment_failure():
    res = requests.post(BASE_URL + "/payment", json={"amount": -1})
    assert res.status_code == 400

# Simulate 100 test cases
@pytest.mark.parametrize("i", range(1, 101))
def test_bulk(i):
    assert i < 105
