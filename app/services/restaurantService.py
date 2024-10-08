from datetime import datetime
import certifi
from pymongo import MongoClient
from app.helpers.exception import RestaurantException
from app.models.restaurauntBaseModel import RestaurantMutation
from app.core.config import settings
from app.helpers.validator import Validator

class RestaurantService:
    def __init__(self):
      self.client = MongoClient(settings.MONGODB_URI, tlsCAFile=certifi.where())
      self.db = self.client[settings.DB_NAME]
      self.collection = self.db["payments"]

    def createRestaurant(self, restaurantMutation : RestaurantMutation, userId : str):
      try:
        restaurantData = restaurantMutation.model_dump()

        if not (Validator.validate_capacity(len(restaurantData["restaurantName"]), 6)):
          raise RestaurantException(400, "Restaurant name must be at least 6 characters long.")
        
        if not Validator.validate_phone_number(restaurantData["contactInfo"]["phoneNumber"]):
          raise RestaurantException(400, "Invalid phone number format.")
                    
        if restaurantData["contactInfo"]["email"] and not Validator.validate_email(restaurantData["contactInfo"]["email"]):
          raise RestaurantException(400, "Invalid email format.")

        if restaurantData["operatingHour"]["openTime"] >= restaurantData["operatingHour"]["closeTime"]:
          raise RestaurantException(400, "Open time must be earlier than close time.")
        
        restaurantData["created_by"] = userId
        restaurantData["created_when"] = datetime.now().strftime("%d%m%Y")  
        restaurantData["updated_when"] = datetime.now().strftime("%d%m%Y")
        restaurantData["status"] = 1
        result = self.collection.insert_one(restaurantData)

        return {"status_code": 201, "restaurant_id": str(result.inserted_id)}
      
      except RestaurantException as e:
            raise e 
      except Exception as e:
          raise RestaurantException(500, f"Error creating restaurant: {str(e)}")
      
    def getRestaurantList(self):
        pass
    
    def getRestaurantById(self, restaurantId : str):
        pass
    
    def updateRestaurant(self, restaurantMutation : RestaurantMutation, restaurantId : str):
        pass
    
    def deleteRestaurant(self, restaurantId : str):
        pass
    
