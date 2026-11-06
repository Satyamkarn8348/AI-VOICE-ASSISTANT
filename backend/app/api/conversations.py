from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.conversation import Conversation
from app.models.user import User
from app.schemas.conversation import ConversationCreate, ConversationResponse

router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.post("/", response_model=ConversationResponse)
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == conversation.user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_conversation = Conversation(
        user_id=conversation.user_id,
        title=conversation.title
    )

    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)

    return new_conversation


@router.get("/", response_model=list[ConversationResponse])
def get_conversations(db: Session = Depends(get_db)):
    return db.query(Conversation).all()
