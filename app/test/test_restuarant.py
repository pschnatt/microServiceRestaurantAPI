import pytest
from fastapi.testclient import TestClient
from app.helpers.exception import RestaurantException
from app.main import app 
from unittest.mock import patch


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

def test_retrieveRestaurant_ReturnSuccess():
    mockResponse = {
        "statusCode": 200,
        "restaurants": [
            {
                "restaurantId": "1234567890abcdef",
                "restaurantName": "Good Eats",
                "location": "123 Food Street",
                "type": "American",
                "contactInfo": {
                    "phoneNumber": "+12345678901",
                    "email": "info@good eats.com"
                },
                "operatingHour": {
                    "openTime": "2024-10-08T09:00:00",
                    "closeTime": "2024-10-08T22:00:00"
                },
                "capacity": 50,
                "description": "A cozy place for delicious food.",
                "createdBy": "userId123",
                "createdWhen": "08102024",
                "updatedWhen": "08102024"
            }
        ]
    }

    with patch('app.services.restaurantService.RestaurantService.getRestaurantList', return_value=mockResponse):
        response = client.get("/api/restaurant/get")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Restaurants fetched successfully",
        "restaurants": mockResponse["restaurants"]
    }

def test_retrieveRestaurant_ReturnFailure():
    mockException = RestaurantException(500, "Error fetching restaurant list.")

    with patch('app.services.restaurantService.RestaurantService.getRestaurantList', side_effect=mockException):
        response = client.get("/api/restaurant/get")

    assert response.status_code == 500
    assert response.json() == {"detail": "Error fetching restaurant list."}

def test_retrieveRestaurantById_ReturnSuccess():
    restaurantId = "1234567890abcdef"
    mockResponse = {
        "statusCode": 200,
        "restaurant": {
            "restaurantId": restaurantId,
            "restaurantName": "Good Eats",
            "location": "123 Food Street",
            "type": "American",
            "contactInfo": {
                "phoneNumber": "+12345678901",
                "email": "info@good eats.com"
            },
            "operatingHour": {
                "openTime": "2024-10-08T09:00:00",
                "closeTime": "2024-10-08T22:00:00"
            },
            "capacity": 50,
            "description": "A cozy place for delicious food.",
            "createdBy": "userId123",
            "createdWhen": "08102024",
            "updatedWhen": "08102024"
        }
    }
    with patch('app.services.restaurantService.RestaurantService.getRestaurantById', return_value=mockResponse):
        response = client.get(f"/api/restaurant/get/{restaurantId}")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Restaurant fetched successfully",
        "restaurant": mockResponse["restaurant"]
    }

def test_retrieveRestaurantById_ReturnFailure():
    restaurantId = "nonexistent_id"
    mockException = RestaurantException(404, "Restaurant not found.")
    with patch('app.services.restaurantService.RestaurantService.getRestaurantById', side_effect=mockException):
        response = client.get(f"/api/restaurant/get/{restaurantId}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Restaurant not found."}

def test_retrieveRestaurantById_ReturnServerError():
    restaurantId = "1234567890abcdef"
    mockException = RestaurantException(500, "Internal server error.")
    with patch('app.services.restaurantService.RestaurantService.getRestaurantById', side_effect=mockException):
        response = client.get(f"/api/restaurant/get/{restaurantId}")
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error."}