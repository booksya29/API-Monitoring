from pydantic import BaseModel


class User(BaseModel):
    id:int | None
    name:str | None
    api_count:int | None
    register_date:None = None