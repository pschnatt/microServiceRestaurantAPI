from pymongo import MongoClient
from bson.objectid import ObjectId
from app.models.restaurauntBaseModel import RestaurantMutation

class RestaurantService:
    def __init__(self):
       pass

    def createRestaurant(self, restaurantMutation : RestaurantMutation):
        pass

    def getRestaurantList(self):
        pass
    
    def getRestaurantById(self, restaurantId : str):
        pass
    
    def updateRestaurant(self, restaurantMutation : RestaurantMutation, restaurantId : str):
        pass
    
    def deleteRestaurant(self, restaurantId : str):
        pass
    
