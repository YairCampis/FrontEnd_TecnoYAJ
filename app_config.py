from pydantic import BaseModel

class AppConfig(BaseModel):
    host:str
    port:int
    
config=AppConfig(host="localhost", port=8000)

print (config.host)
print (config.port)