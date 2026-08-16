from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)


class UserResponse(BaseModel):
    id: int
    username: str


class MessageCreate(BaseModel):
    sender: str = Field(min_length=3, max_length=30)
    receiver: str = Field(min_length=3, max_length=30)
    content: str = Field(min_length=1, max_length=1000)


class MessageResponse(BaseModel):
    id: int
    sender: str
    receiver: str
    content: str