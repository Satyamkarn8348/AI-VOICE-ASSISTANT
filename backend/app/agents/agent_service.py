
import re
import ollama

from app.tools.calculator import calculate
from app.core.creator_profile import CREATOR_PROFILE


MODEL_NAME = "llama3.2"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": (
                "Calculate mathematical expressions accurately. "
                "Use only for actual arithmetic operations."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


def get_latest_user_message(user_input):

    if isinstance(user_input, str):
        return user_input.strip()

    if isinstance(user_input, list):
        for message in reversed(user_input):
            if message.get("role") == "user":
                return str(message.get("content", "")).strip()

    return ""


def is_creator_question(message: str) -> bool:

    text = message.lower().strip()

    creator_keywords = [
        "creator",
        "created you",
        "who made you",
        "who developed you",
        "your developer",
        "your owner",
        "tumhe kisne banaya",
        "tumko kisne banaya",
        "tumhe kisne create kiya",
        "tumhara creator",
        "tumhare creator",
        "kisne banaya hai",
        "kisne create kiya"
    ]

    return any(keyword in text for keyword in creator_keywords)


def get_creator_response(message: str) -> str:

    profile = CREATOR_PROFILE
    text = message.lower()

    hindi_words = [
        "tum", "aap", "kaun", "kisne", "banaya",
        "batao", "baare", "mein", "kya", "hai"
    ]

    is_hinglish = any(
        word in text.split() for word in hindi_words
    )

    if is_hinglish:
        return (
            f"Mujhe {profile['name']} ne banaya hai. "
            f"Unki age {profile['age']} years hai. "
            f"Unhone {profile['education']} kiya hai. "
            f"Woh {profile['location']} mein rehte hain."
        )

    return (
        f"My creator is {profile['name']}. "
        f"He is {profile['age']} years old. "
        f"He has completed {profile['education']}. "
        f"He lives in {profile['location']}."
    )


def is_calculation_request(message: str) -> bool:

    text = message.lower().strip()

    # Direct arithmetic expressions
    if re.search(r"\d+\s*[\+\*/%]\s*\d+", text):
        return True

    if re.search(r"\d+\s*-\s*\d+", text):
        return True

    # Common calculation phrases
    calculation_keywords = [
        "calculate",
        "calculator",
        "solve",
        "what is the value",
        "kitna hota hai",
        "kitna hoga",
        "jod",
        "guna",
        "multiply",
        "divide",
        "percentage",
        "percent of",
        "square root",
        "calculate karo"
    ]

    return any(
        keyword in text
        for keyword in calculation_keywords
    )


def generate_agent_response(user_input) -> str:

    latest_message = get_latest_user_message(user_input)

    # Creator questions do not need an LLM call
    if is_creator_question(latest_message):
        print("Agent Selected: Creator Profile")
        return get_creator_response(latest_message)

    system_instruction = """
You are a helpful personal AI assistant.

CALCULATOR RULES:
- Use calculate only for actual mathematical calculations.
- Never use calculate for normal questions.
- Never show tool-call JSON to the user.
- Explain calculation results clearly.

GENERAL RULES:
- Answer naturally in the user's language.
- Never invent personal information.
- Never show internal tool details to the user.
"""

    if isinstance(user_input, str):

        messages = [
            {
                "role": "system",
                "content": system_instruction
            },
            {
                "role": "user",
                "content": user_input.strip()
            }
        ]

    elif isinstance(user_input, list):

        messages = user_input.copy()

        messages.insert(
            1 if messages and messages[0].get("role") == "system" else 0,
            {
                "role": "system",
                "content": system_instruction
            }
        )

    else:
        raise TypeError("Input must be a string or messages list")

    try:

        # Normal questions: direct model call without tools
        if not is_calculation_request(latest_message):

            print("Agent Selected: Direct LLM Response")

            response = ollama.chat(
                model=MODEL_NAME,
                messages=messages,
                options={
                    "temperature": 0,
                    "top_p": 0.9,
                    "num_predict": 500,
                    "num_ctx": 2048
                }
            )

            return (
                response.message.content or ""
            ).strip()

        # Calculation questions: enable calculator tool
        print("Agent Selected: Calculator")

        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS,
            options={
                "temperature": 0,
                "top_p": 0.9,
                "num_predict": 300,
                "num_ctx": 2048
            }
        )

        assistant_message = response.message
        tool_calls = assistant_message.tool_calls or []

        if not tool_calls:
            return (assistant_message.content or "").strip()

        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        for tool_call in tool_calls:

            function_name = tool_call.function.name
            arguments = tool_call.function.arguments

            if function_name == "calculate":

                expression = arguments.get("expression", "")

                if (
                    not isinstance(expression, str)
                    or not expression.strip()
                ):
                    result = "Error: Invalid expression"
                else:
                    result = calculate(expression)

            else:
                result = "Error: Unknown tool"

            messages.append({
                "role": "tool",
                "tool_name": function_name,
                "content": str(result)
            })

        # Get final answer using calculator result
        final_response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            options={
                "temperature": 0,
                "num_predict": 250,
                "num_ctx": 2048
            }
        )

        return (
            final_response.message.content or ""
        ).strip()

    except Exception as error:

        print("Agent Error:", repr(error))

        return (
            "Sorry, mujhe abhi answer generate karne mein "
            "problem ho rahi hai."
        )
