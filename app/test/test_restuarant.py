from fastapi.testclient import TestClient
from app.helpers.exception import RestaurantException
from main import app 
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
        "description": "A cozy place for delicious food.",
        "cost" : 1
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
        "description": "A cozy place for delicious food.",
        "cost" : 1
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
                "cost" : 1,
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
            "cost" : 1,
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

def test_updateRestaurant_ReturnSuccess():
    mock_response = {
        "statusCode": 200,
        "restaurantId": "1234567890abcdef"
    }

    with patch('app.services.restaurantService.RestaurantService.updateRestaurant', return_value=mock_response):
        restaurant_data = {
            "restaurantName": "Updated Restaurant",
            "location": "123 Updated Food Street",
            "type": "Italian",
            "contactInfo": {
                "phoneNumber": "+12345678901",
                "email": "info@updatedrestaurant.com"
            },
            "operatingHour": {
                "openTime": "2024-10-08T09:00:00",
                "closeTime": "2024-10-08T22:00:00"
            },
            "capacity": 50,
            "description": "An updated description.",
            "cost" : 1
        }

        response = client.put("/api/restaurant/userId123/update/1234567890abcdef", json=restaurant_data)

    assert response.status_code == 200
    assert response.json() == {"message" : "Restaurant updated successfully","restaurantId": "1234567890abcdef"}

def test_updateRestaurant_ReturnFailure_RestaurantInactive():
    mock_exception = RestaurantException(400, "Cannot update restaurant because it is inactive.")

    with patch('app.services.restaurantService.RestaurantService.updateRestaurant', side_effect=mock_exception):
        restaurant_data = {
            "restaurantName": "Inactive Restaurant",
            "location": "123 Inactive Food Street",
            "type": "Italian",
            "contactInfo": {
                "phoneNumber": "+12345678901",
                "email": "info@inactiverestaurant.com"
            },
            "operatingHour": {
                "openTime": "2024-10-08T09:00:00",
                "closeTime": "2024-10-08T22:00:00"
            },
            "capacity": 50,
            "description": "An inactive restaurant.",
            "cost" : 1
        }

        response = client.put("/api/restaurant/userId123/update/1234567890abcdef", json=restaurant_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot update restaurant because it is inactive."}

def test_updateRestaurant_ReturnFailure_InvalidData():
    mock_exception = RestaurantException(400, "Restaurant name must be at least 6 characters long.")

    with patch('app.services.restaurantService.RestaurantService.updateRestaurant', side_effect=mock_exception):
        restaurant_data = {
            "restaurantName": "Bad",
            "location": "123 Bad Food Street",
            "type": "Italian",
            "contactInfo": {
                "phoneNumber": "+12345678901",
                "email": "info@badrestaurant.com"
            },
            "operatingHour": {
                "openTime": "2024-10-08T09:00:00",
                "closeTime": "2024-10-08T22:00:00"
            },
            "capacity": 50,
            "description": "A bad restaurant.",
            "cost" : 1
        }

        response = client.put("/api/restaurant/userId123/update/1234567890abcdef", json=restaurant_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Restaurant name must be at least 6 characters long."}

def test_deleteRestaurant_ReturnSuccess():
    mockResponse = {
        "statusCode": 200,
        "restaurantId": "1234567890abcdef"
    }

    with patch('app.services.restaurantService.RestaurantService.deleteRestaurant', return_value=mockResponse):
        response = client.delete("/api/restaurant/userId123/delete/1234567890abcdef")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Restaurant deleted successfully",
        "restaurantId": mockResponse["restaurantId"]
    }

def test_deleteRestaurant_ReturnFailure():
    mockException = RestaurantException(404, "Restaurant not found.")

    with patch('app.services.restaurantService.RestaurantService.deleteRestaurant', side_effect=mockException):
        response = client.delete("/api/restaurant/userId123/delete/1234567890abcdef")

    assert response.status_code == 404
    assert response.json() == {"detail": "Restaurant not found."}