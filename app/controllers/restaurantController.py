from fastapi import APIRouter

from app.models.restaurauntBaseModel import RestaurantMutation
from app.services.restaurantService import RestaurantService

router = APIRouter()

payment_service = RestaurantService()

@router.post("/create")
async def addRestaurant(restaurantMutation : RestaurantMutation):
    pass

@router.get("/get")
async def retrieveRestaurant():
    pass

@router.get("/get/{restaurantId}")
async def retrieveRestaurantById(restaurantId: str):
    pass

@router.patch("/update/{restaurantId}")
async def updateRestaurant(restaurantMutation : RestaurantMutation, restaurantId: str):
    pass

@router.delete("/delete/{restaurantId}")
async def deleteRestaurant(restaurantId: str):
    pass
