from pydantic import BaseModel


class ConversationCreate(BaseModel):
    user_id: int
    title: str


class ConversationResponse(BaseModel):
    id: int
    user_id: int
    title: str | None = None

    class Config:
        from_attributes = True