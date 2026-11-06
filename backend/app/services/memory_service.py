from sqlalchemy.orm import Session
from app.models.memory import Memory


def save_memory(
    db: Session,
    user_id: int,
    category: str,
    memory_key: str,
    memory_value: str
):
    memory = db.query(Memory).filter(
        Memory.user_id == user_id,
        Memory.memory_key == memory_key
    ).first()

    if memory:
        memory.category = category
        memory.memory_value = memory_value
    else:
        memory = Memory(
            user_id=user_id,
            category=category,
            memory_key=memory_key,
            memory_value=memory_value
        )
        db.add(memory)

    db.commit()
    db.refresh(memory)

    return memory


def save_memories(
    db: Session,
    user_id: int,
    memories: list[dict]
):
    if not memories:
        return []

    memory_keys = [
        item["memory_key"]
        for item in memories
    ]

    existing_memories = db.query(Memory).filter(
        Memory.user_id == user_id,
        Memory.memory_key.in_(memory_keys)
    ).all()

    existing_map = {
        memory.memory_key: memory
        for memory in existing_memories
    }

    saved_memories = []

    for item in memories:
        memory_key = item["memory_key"]

        if memory_key in existing_map:
            memory = existing_map[memory_key]
            memory.category = item["category"]
            memory.memory_value = item["memory_value"]
        else:
            memory = Memory(
                user_id=user_id,
                category=item["category"],
                memory_key=memory_key,
                memory_value=item["memory_value"]
            )
            db.add(memory)

        saved_memories.append(memory)

    db.commit()

    return saved_memories


def get_user_memories(db: Session, user_id: int):
    return db.query(Memory).filter(
        Memory.user_id == user_id
    ).order_by(
        Memory.updated_at.desc()
    ).all()


def format_memories_for_prompt(memories: list[Memory]) -> str:
    if not memories:
        return "No saved memories available."

    return "\n".join(
        f"- {memory.category}: {memory.memory_key} = {memory.memory_value}"
        for memory in memories
    )