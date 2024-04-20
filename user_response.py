from pydantic import BaseModel

class UserResponse(BaseModel):
    username:str
    email:str
    

user_response=UserResponse(username="Yair", email="yaircampis@gmail.com")

print (user_response.json())
