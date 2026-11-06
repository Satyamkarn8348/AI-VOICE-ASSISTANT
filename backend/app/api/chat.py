
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.models.conversation import Conversation
from app.models.message import Message

from app.schemas.chat import ChatRequest, ChatResponse

from app.services.chat_service import (
    generate_response,
    generate_related_questions
)

from app.services.memory_service import (
    get_user_memories,
    format_memories_for_prompt,
    save_memories
)

from app.services.memory_extractor import extract_memories


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    # Find conversation
    conversation = db.query(Conversation).filter(
        Conversation.id == request.conversation_id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    # Extract useful memories
    extracted_memories = extract_memories(request.message)

    # Save all memories in one batch
    save_memories(
        db=db,
        user_id=conversation.user_id,
        memories=extracted_memories
    )

    # Get latest 10 conversation messages
    previous_messages = db.query(Message).filter(
        Message.conversation_id == request.conversation_id
    ).order_by(
        Message.id.desc()
    ).limit(10).all()

    # Restore chronological order
    previous_messages.reverse()

    chat_history = [
        {
            "role": message.role,
            "content": message.content
        }
        for message in previous_messages
    ]

    # Get updated user memories
    memories = get_user_memories(
        db,
        conversation.user_id
    )

    user_memories = format_memories_for_prompt(memories)

    # Generate AI answer
    response = generate_response(
        request.message,
        chat_history,
        user_memories
    )

    # Generate related questions
    related_questions = generate_related_questions(
        request.message,
        response,
        chat_history
    )

    # Save user message
    db.add(
        Message(
            conversation_id=request.conversation_id,
            role="user",
            content=request.message
        )
    )

    # Save assistant response
    db.add(
        Message(
            conversation_id=request.conversation_id,
            role="assistant",
            content=response
        )
    )

    db.commit()

    # Return answer and related questions
    return ChatResponse(
        response=response,
        related_questions=related_questions
    )
