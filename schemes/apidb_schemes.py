from pydantic import BaseModel
from datetime import datetime
class ApiScheme(BaseModel):
    id:int | None = None
    creator_id:int 
    status:bool | None = True
    url:str
    send_method:str
    body:str
    created_at:None = None
    max_delay:int = 360

class ApiResponse_scheme(BaseModel):
    request_id:int = None
    status_code:int
    answer:str = None
    check_time:datetime = None
    def __call__(self):
        print(self)