
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database.connection import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

from app.services.memory_service import (
    save_memory,
    get_user_memories
)

router = APIRouter()


class MemorySaveRequest(BaseModel):
    user_id: int
    category: str = Field(min_length=1, max_length=50)
    memory_key: str = Field(min_length=1, max_length=100)
    memory_value: str = Field(min_length=1)


@router.get("/")
def home():
    return {
        "message": "Welcome to AI Voice Assistant!"
    }


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Backend is running successfully"
    }


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    new_user = User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Save user memory
@router.post("/memories")
def create_memory(
    request: MemorySaveRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == request.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    memory = save_memory(
        db=db,
        user_id=request.user_id,
        category=request.category,
        memory_key=request.memory_key,
        memory_value=request.memory_value
    )

    return {
        "message": "Memory saved successfully!",
        "memory": {
            "id": memory.id,
            "category": memory.category,
            "key": memory.memory_key,
            "value": memory.memory_value
        }
    }


# Get saved user memories
@router.get("/memories/{user_id}")
def read_memories(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    memories = get_user_memories(db, user_id)

    return {
        "total_memories": len(memories),
        "memories": [
            {
                "id": memory.id,
                "category": memory.category,
                "key": memory.memory_key,
                "value": memory.memory_value
            }
            for memory in memories
        ]
    }
