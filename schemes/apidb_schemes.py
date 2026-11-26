from pydantic import BaseModel

class ApiScheme(BaseModel):
    id:int | None = None
    creator_id:int 
    status:bool | None = True
    url:str
    send_method:str
    body:str
    created_at:None = None