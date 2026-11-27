from pydantic import BaseModel
from datetime import datetime

class HistoryScheme(BaseModel):
    id:int|None = None
    api_id:int
    status_code:int
    body:str
    check_time:datetime = None
    user_id:int