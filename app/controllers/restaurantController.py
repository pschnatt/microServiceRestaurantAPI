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
      return JSONResponse(status_code=response["status_code"], content={"message": "Restaurant created successfully", "restaurantId": response["restaurant_id"]})
    
    except RestaurantException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/get")
async def retrieveRestaurant():
    pass

@router.get("/get/{restaurantId}")
async def retrieveRestaurantById(restaurantId: str):
    pass

@router.patch("/{userId}/update/{restaurantId}")
async def updateRestaurant(restaurantMutation : RestaurantMutation, restaurantId: str, userId : str):
    pass

@router.delete("/{userId}/delete/{restaurantId}")
async def deleteRestaurant(restaurantId: str, userId : str):
    pass
