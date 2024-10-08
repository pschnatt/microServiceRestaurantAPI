import re

class Validator:

  @staticmethod
  def validate_phone_number(phone_number: str) -> bool:
        pattern = r'^\+?\d{10,15}$'  # Example: +66835454248 or 0835454248
        return re.match(pattern, phone_number) is not None
    
  @staticmethod  
  def validate_email(email: str) -> bool:
      pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
      return re.match(pattern, email) is not None
  
  @staticmethod
  def validate_capacity(capacity: int, min_limit: int) -> bool:
        return capacity >= min_limit
  