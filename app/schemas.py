from pydantic import BaseModel, EmailStr, constr


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    text: constr(min_length=1, max_length=1_000_000)  # max 1MB payload approx


class PostRead(BaseModel):
    postID: int
    text: str
