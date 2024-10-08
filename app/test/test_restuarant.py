import pytest
from fastapi.testclient import TestClient
from app.main import app 

client = TestClient(app)

def test_addRestaurant_ReturnSuccess():
    userId = 1
    restaurantData = {
        "restaurantName": "Good Eats",
        "location": "123 Food Street",
        "type": "American",
        "contactInfo": {
            "phoneNumber": "+12345678901",
            "email": "info@goodeats.com"
        },
        "operatingHour": {
            "openTime": "2024-10-08T09:00:00",
            "closeTime": "2024-10-08T22:00:00"
        },
        "capacity": 50,
        "description": "A cozy place for delicious food."
    }
    response = client.post(f"/api/restaurant/{userId}/create", json=restaurantData)

    assert response.status_code == 201
    assert "restaurantId" in response.json()

def test_addRestaurantInvalidName_ReturnError():
    userId = 1
    restaurantData = {
        "restaurantName": "Eats",
        "location": "123 Food Street",
        "type": "American",
        "contactInfo": {
            "phoneNumber": "+12345678901",
            "email": "info@goodeats.com"
        },
        "operatingHour": {
            "openTime": "2024-10-08T09:00:00",
            "closeTime": "2024-10-08T22:00:00"
        },
        "capacity": 50,
        "description": "A cozy place for delicious food."
    }
    response = client.post(f"/api/restaurant/{userId}/create", json=restaurantData)

    assert response.status_code == 400
    assert response.json()["detail"] == "Restaurant name must be at least 6 characters long."

