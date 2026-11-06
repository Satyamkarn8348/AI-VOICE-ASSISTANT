from app.agents.agent_service import generate_agent_response


questions = [
    "What is 1250 multiplied by 24?",
    "What is Python?"
]

for question in questions:

    print("\nUser:", question)

    response = generate_agent_response(question)

    print("Robot:", response)