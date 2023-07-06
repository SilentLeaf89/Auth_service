from pydantic import BaseModel, Field


class Login(BaseModel):
    login: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=3, max_length=255)

    class Config:
        orm_mode = True


class Change(BaseModel):
    old_password: str = Field(min_length=3, max_length=255)
    new_login: str = Field(min_length=3, max_length=255)
    new_password: str = Field(min_length=3, max_length=255)

    class Config:
        orm_mode = True
