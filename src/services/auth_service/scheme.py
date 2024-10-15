from pydantic import BaseModel


class SUserResponse(BaseModel):
    id: int
    username: str