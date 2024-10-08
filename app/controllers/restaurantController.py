from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.helpers.exception import RestaurantException
from app.models.restaurauntBaseModel import RestaurantMutation
from app.services.restaurantService import RestaurantService

router = APIRouter()

restaurantService = RestaurantService()

@router.post("/{userId}/create")
async def addRestaurant(restaurantMutation : RestaurantMutation, userId: str):
    try:
      response = restaurantService.createRestaurant(restaurantMutation, userId)
      return JSONResponse(status_code=response["statusCode"], content={"message": "Restaurant created successfully", "restaurantId": response["restaurantId"]})
    except RestaurantException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/get")
async def retrieveRestaurant():
    try:
        response = restaurantService.getRestaurantList()
        return JSONResponse(status_code=response["statusCode"], content={"message": "Restaurants fetched successfully", "restaurants": response["restaurants"]})
    except RestaurantException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/get/{restaurantId}")
async def retrieveRestaurantById(restaurantId: str):
    try:
        response = restaurantService.getRestaurantById(restaurantId)
        return JSONResponse(status_code=response["statusCode"], content={"message": "Restaurant fetched successfully", "restaurant": response["restaurant"]})
    except RestaurantException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{userId}/update/{restaurantId}")
async def updateRestaurant(restaurantMutation : RestaurantMutation, restaurantId: str, userId : str):
    try:
        response = restaurantService.updateRestaurant(restaurantMutation, restaurantId, userId)
        return JSONResponse(status_code=response["statusCode"], content={"restaurantId": response["restaurantId"]})
    except RestaurantException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{userId}/delete/{restaurantId}")
async def deleteRestaurant(restaurantId: str, userId : str):
    pass
