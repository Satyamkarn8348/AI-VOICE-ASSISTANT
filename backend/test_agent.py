import ollama
from app.tools.calculator import calculate


tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate mathematical expressions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


def run_agent(user_message: str):

    print("\nUser:", user_message)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant. "
                "You must use the calculate tool for mathematical calculations. "
                "Never return tool calls as JSON text."
            )
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    response = ollama.chat(
        model="llama3.2",
        messages=messages,
        tools=tools
    )

    assistant_message = response.message
    tool_calls = assistant_message.tool_calls or []

    print("\nDetected tool calls:", len(tool_calls))

    if not tool_calls:
        print("\nAI:", assistant_message.content)
        return

    messages.append(
        assistant_message.model_dump(exclude_none=True)
    )

    for tool_call in tool_calls:

        function_name = tool_call.function.name
        arguments = tool_call.function.arguments

        if function_name == "calculate":

            expression = arguments["expression"]

            print("\nAgent selected:", function_name)
            print("Expression:", expression)

            result = calculate(expression)

            print("Calculator result:", result)

            messages.append({
                "role": "tool",
                "tool_name": function_name,
                "content": result
            })

    final_response = ollama.chat(
        model="llama3.2",
        messages=messages
    )

    print("\nFinal AI Response:", final_response.message.content)


if __name__ == "__main__":
    run_agent("What is 1250 multiplied by 24?")
