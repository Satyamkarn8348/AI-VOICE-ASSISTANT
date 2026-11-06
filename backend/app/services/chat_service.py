
import ollama

from app.agents.agent_service import generate_agent_response


MODEL_NAME = "llama3.2"


def is_song_request(message: str) -> bool:

    text = message.lower().strip()

    song_keywords = [
        "gana", "gaana", "song",
        "गाना", "गाने", "गीत"
    ]

    action_keywords = [
        "gao", "gaao", "sunao", "sunaao", "sing",
        "गा के सुनाओ", "गाकर सुनाओ", "गाओ", "सुनाओ",
        "गा दो"
    ]

    if "sing a song" in text:
        return True

    return (
        any(word in text for word in song_keywords)
        and any(action in text for action in action_keywords)
    )


def generate_response(
    message: str,
    chat_history: list[dict[str, str]],
    user_memories: str = "No saved memories available."
) -> str:

    song_mode = is_song_request(message)

    song_instruction = ""

    if song_mode:
        song_instruction = """
SONG MODE:
1. Generate a completely original Hindi song.
2. Write only in Roman Hindi using English letters.
3. Generate approximately 6 to 8 meaningful lines.
4. Make the lyrics rhythmic and enjoyable.
5. Do not copy existing copyrighted song lyrics.
6. Return only the lyrics without extra explanation.
"""

    normal_instruction = """
GENERAL QUESTION ANSWERING:

1. Understand the complete question.
2. Give accurate, relevant and complete answers.
3. Never invent facts, dates, names or statistics.
4. If unsure, clearly say that you are unsure.
5. Never present guesses as verified facts.
6. Answer every part of multiple questions.
7. Explain complex topics step by step.
8. Use examples when helpful.
9. Avoid unrelated information and repetition.
10. Never stop an answer in the middle.
11. Understand follow-up questions using conversation history.
12. Ask for clarification when the question is ambiguous.
13. For coding requests, provide complete working code.
14. Never replace a coding request with only an explanation.

AGENTIC AI:

1. Use the calculate tool for mathematical calculations.
2. Use it only when an actual calculation is required.
3. Never guess mathematical results.
4. For normal questions, answer directly.
5. Never show tool-call JSON to the user.

LANGUAGE:

1. Reply in simple English when the user speaks English.
2. Reply in natural Hinglish using English letters
   when the user speaks Hindi or Hinglish.
3. Never use Devanagari script.
4. Keep answers natural and easy to understand.
"""

    system_prompt = f"""
You are a friendly, intelligent and reliable personal AI
Voice Assistant.

USER MEMORY:
{user_memories}

Use saved memories only when relevant.
Never invent personal information.

{normal_instruction}

{song_instruction}
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    # Add valid conversation history
    valid_history = []

    for item in chat_history[-10:]:

        role = item.get("role")
        content = item.get("content")

        if (
            role in ("user", "assistant")
            and isinstance(content, str)
            and content.strip()
        ):
            valid_history.append({
                "role": role,
                "content": content
            })

    messages.extend(valid_history)

    # Add current user message
    messages.append({
        "role": "user",
        "content": message.strip()
    })

    # Song requests bypass Agentic AI tools
    if song_mode:

        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            options={
                "temperature": 0.7,
                "top_p": 0.9,
                "repeat_penalty": 1.1,
                "num_predict": 250,
                "num_ctx": 2048
            }
        )

        answer = response.message.content.strip()

    else:

        # Normal requests use Agent Service
        answer = generate_agent_response(messages)

    if not answer:
        return "Sorry, mujhe abhi answer generate karne mein problem ho rahi hai."

    return answer


def generate_related_questions(
    message: str,
    answer: str,
    chat_history: list[dict[str, str]]
) -> list[str]:

    # No suggestions for song requests
    if is_song_request(message):
        return []

    text = message.lower().strip()

    # Lightweight rule-based suggestions
    if any(word in text for word in [
        "python", "java", "javascript", "react",
        "spring boot", "programming", "coding"
    ]):
        return [
            "Can you explain this with an example?",
            "What are the important concepts related to this?",
            "Where is this used in real projects?"
        ]

    if any(word in text for word in [
        "who", "what", "why", "when", "where", "how"
    ]):
        return [
            "Can you explain this in more detail?",
            "Can you give me a practical example?",
            "What else should I know about this topic?"
        ]

    return [
        "Can you explain this further?",
        "Can you give me an example?",
        "What should I learn next?"
    ]
