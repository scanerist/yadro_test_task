from pydantic import BaseModel

class UserBase(BaseModel):
    gender: str
    first_name: str
    last_name: str
    phone: str
    email: str
    location: str
    picture: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True