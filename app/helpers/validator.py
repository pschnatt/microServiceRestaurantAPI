import re

class Validator:

  @staticmethod
  def validatePhoneNumber(phone_number: str) -> bool:
        pattern = r'^\+?\d{10,15}$'
        return re.match(pattern, phone_number) is not None
    
  @staticmethod  
  def validateEmail(email: str) -> bool:
      pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
      return re.match(pattern, email) is not None
  
  @staticmethod
  def validateCapacity(capacity: int, min_limit: int) -> bool:
        return capacity >= min_limit
  