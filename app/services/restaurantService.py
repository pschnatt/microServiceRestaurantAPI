from datetime import datetime
from bson import ObjectId
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

        if not (Validator.validateCapacity(len(restaurantData["restaurantName"]), 6)):
          raise RestaurantException(400, "Restaurant name must be at least 6 characters long.")
        
        if not Validator.validatePhoneNumber(restaurantData["contactInfo"]["phoneNumber"]):
          raise RestaurantException(400, "Invalid phone number format.")
                    
        if restaurantData["contactInfo"]["email"] and not Validator.validateEmail(restaurantData["contactInfo"]["email"]):
          raise RestaurantException(400, "Invalid email format.")

        if restaurantData["operatingHour"]["openTime"] >= restaurantData["operatingHour"]["closeTime"]:
          raise RestaurantException(400, "Open time must be earlier than close time.")
        
        restaurantData["created_by"] = userId
        restaurantData["created_when"] = datetime.now().strftime("%d%m%Y") 
        restaurantData["updated_by"] = userId 
        restaurantData["updated_when"] = datetime.now().strftime("%d%m%Y")
        restaurantData["status"] = 1
        result = self.collection.insert_one(restaurantData)

        return {"statusCode": 201, "restaurantId": str(result.inserted_id)}
      
      except RestaurantException as e:
            raise e 
      except Exception as e:
          raise RestaurantException(500, f"Error creating restaurant: {str(e)}")
      
    def getRestaurantList(self):
      try:
        restaurants = list(self.collection.find({"status": 1}))
        restaurantList = [{
            "restaurantId": str(restaurant["_id"]),
            "restaurantName": restaurant["restaurantName"],
            "location": restaurant["location"],
            "type": restaurant["type"],
            "contactInfo": restaurant["contactInfo"],
            "operatingHour": restaurant["operatingHour"],
            "capacity": restaurant["capacity"],
            "description": restaurant["description"],
            "createdBy": restaurant["createdBy"],
            "createdWhen": restaurant["createdWhen"],
            "updatedBy": restaurant["updatedBy"],
            "updatedWhen": restaurant["updatedWhen"]
        } for restaurant in restaurants]

        return {"statusCode": 200, "restaurants": restaurantList}  
    
      except Exception as e:
        raise RestaurantException(500, f"Error fetching restaurant list: {str(e)}")
    
    def getRestaurantById(self, restaurantId: str):
        try:
            restaurant = self.collection.find_one({"_id": ObjectId(restaurantId), "status": 1})
            
            if restaurant is None:
                raise RestaurantException(404, "Restaurant not found.")
            
            restaurantData = {
                "restaurantId": str(restaurant["_id"]),
                "restaurantName": restaurant["restaurantName"],
                "location": restaurant["location"],
                "type": restaurant["type"],
                "contactInfo": restaurant["contactInfo"],
                "operatingHour": restaurant["operatingHour"],
                "capacity": restaurant["capacity"],
                "description": restaurant["description"],
                "createdBy": restaurant["createdBy"],
                "createdWhen": restaurant["createdWhen"],
                "updatedBy": restaurant["updatedBy"],
                "updatedWhen": restaurant["updatedWhen"]
            }
            return {"statusCode": 200, "restaurant": restaurantData}
        
        except RestaurantException as e:
            raise e
        except Exception as e:
            raise RestaurantException(500, f"Error fetching restaurant by ID: {str(e)}")
    
    def updateRestaurant(self, restaurantMutation: RestaurantMutation, restaurantId: str, userId: str):
        try:
            restaurantData = restaurantMutation.model_dump()

            if not (Validator.validateCapacity(len(restaurantData["restaurantName"]), 6)):
                raise RestaurantException(400, "Restaurant name must be at least 6 characters long.")
            
            if not Validator.validatePhoneNumber(restaurantData["contactInfo"]["phoneNumber"]):
                raise RestaurantException(400, "Invalid phone number format.")
            
            if restaurantData["contactInfo"]["email"] and not Validator.validate_email(restaurantData["contactInfo"]["email"]):
                raise RestaurantException(400, "Invalid email format.")

            if restaurantData["operatingHour"]["openTime"] >= restaurantData["operatingHour"]["closeTime"]:
                raise RestaurantException(400, "Open time must be earlier than close time.")
            
            existing_restaurant = self.collection.find_one({"_id": ObjectId(restaurantId)})
            if not existing_restaurant:
                raise RestaurantException(404, "Restaurant not found.")
            if existing_restaurant["status"] == 0:
                raise RestaurantException(400, "Cannot update restaurant because it is inactive.")

            updateData = {
                "$set": {
                    "restaurantName": restaurantData["restaurantName"],
                    "location": restaurantData["location"],
                    "type": restaurantData["type"],
                    "contactInfo": restaurantData["contactInfo"],
                    "operatingHour": restaurantData["operatingHour"],
                    "capacity": restaurantData["capacity"],
                    "description": restaurantData["description"],
                    "updated_by" : userId,
                    "updated_When": datetime.now().strftime("%d%m%Y") 
                }
            }

            result = self.collection.update_one({"_id": ObjectId(restaurantId)}, updateData)

            return {"statusCode": 200, "restaurantId": restaurantId}

        except RestaurantException as e:
            raise e
        except Exception as e:
            raise RestaurantException(500, f"Error updating restaurant: {str(e)}")
    
    def deleteRestaurant(self, restaurantId : str):
        pass
    
