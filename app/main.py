from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

from app.dependencies import get_current_user
from app.schemas import UserCreate, UserRead, PostCreate, PostRead
from app.auth import hash_password, verify_password, create_token
from app.memory_store import InMemoryPostStore


app = FastAPI()

# In-memory "database" for users and posts
users_db = {}
post_store = InMemoryPostStore()


@app.get("/")
def read_root():
    """Return a welcome message."""
    return {"message": "Welcome to FastPost!"}


@app.post("/register", response_model=UserRead)
def register(user: UserCreate):
    """Register a new user, hash password, return user data."""
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user.password)
    user_id = len(users_db) + 1
    users_db[user.email] = {
        "id": user_id,
        "email": user.email,
        "hashed_password": hashed,
    }
    return {"id": user_id, "email": user.email}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return JWT token if valid."""
    user = users_db.get(form_data.username)
    if not user or not verify_password(
        form_data.password, user["hashed_password"]
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/posts", response_model=PostRead)
def create_post(
    post: PostCreate, current_user: dict = Depends(get_current_user)
):
    """Add a new post for the authenticated user."""
    post_id = post_store.add_post(current_user["sub"], post.text)
    return {"postID": post_id, "text": post.text}


@app.get("/posts", response_model=List[PostRead])
def get_posts(current_user: dict = Depends(get_current_user)):
    """Get all posts belonging to the authenticated user."""
    return post_store.get_posts_for_user(current_user["sub"])


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, current_user: dict = Depends(get_current_user)):
    """Delete a user's post by post ID, error if not found or unauthorized."""
    success = post_store.delete_post(current_user["sub"], post_id)
    if not success:
        raise HTTPException(
            status_code=404, detail="Post not found or unauthorized"
        )
    return {"detail": "Post deleted"}
