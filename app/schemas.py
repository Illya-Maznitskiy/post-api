from pydantic import BaseModel, EmailStr, constr


class UserCreate(BaseModel):
    """Schema for user signup with email and password validation."""
    email: EmailStr
    password: constr(min_length=8)


class UserRead(BaseModel):
    """Schema for reading user data with ID and email."""
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    """Schema for creating a post with text (1 to ~1MB)."""
    text: constr(min_length=1, max_length=1_000_000)


class PostRead(BaseModel):
    """Schema for reading a post with ID and text."""
    postID: int
    text: str
