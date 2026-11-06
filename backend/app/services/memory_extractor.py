
import json
import ollama
import re


MODEL_NAME = "llama3.2"


# Messages that do not need memory extraction
SKIP_KEYWORDS = [
    "hello", "hi", "hey", "good morning",
    "good evening", "good night",
    "thank you", "thanks", "bye",
    "what is", "what are", "how to",
    "explain", "calculate", "solve",
    "who is", "where is", "when is"
]


def should_extract_memory(message: str) -> bool:

    text = message.lower().strip()

    if len(text.split()) < 4:
        return False

    if any(keyword in text for keyword in SKIP_KEYWORDS):
        return False

    return True


def extract_memories(user_message: str) -> list[dict]:

    if not should_extract_memory(user_message):
        return []

    prompt = f"""
Extract useful, stable facts explicitly shared by the user
about themselves.

Rules:
1. Extract only clear personal facts.
2. Extract stable preferences, interests and goals.
3. Ignore questions and hypothetical statements.
4. Ignore temporary information and facts about others.
5. Never extract sensitive personal information.
6. If no suitable fact exists, return an empty array.
7. Never invent information.

Return JSON:
{{
    "memories": [
        {{
            "category": "personal",
            "memory_key": "example",
            "memory_value": "example"
        }}
    ]
}}

User message:
{user_message}
"""

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            format="json",
            options={
                "temperature": 0,
                "num_predict": 120,
                "num_ctx": 1024
            }
        )

        content = response["message"]["content"]
        extracted = json.loads(content)

        if isinstance(extracted, dict):
            extracted = extracted.get("memories", [])

        if not isinstance(extracted, list):
            return []

        valid_memories = []

        allowed_categories = {
            "personal",
            "language",
            "preferences",
            "interests",
            "goals",
            "work",
            "education"
        }

        for item in extracted:

            if not isinstance(item, dict):
                continue

            category = item.get("category")
            memory_key = item.get("memory_key")
            memory_value = item.get("memory_value")

            if not all(
                isinstance(value, str) and value.strip()
                for value in [category, memory_key, memory_value]
            ):
                continue

            if category.strip().lower() not in allowed_categories:
                continue

            valid_memories.append({
                "category": category.strip().lower()[:50],
                "memory_key": memory_key.strip()[:100],
                "memory_value": memory_value.strip()[:1000]
            })

        return valid_memories

    except Exception as error:
        print(f"Memory extraction failed: {error}")
        return []
