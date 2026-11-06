
import json
import re
import ollama


MODEL_NAME = "llama3.2"


PROJECT_SCHEMA = {
    "type": "object",
    "properties": {
        "project_name": {
            "type": "string"
        },
        "description": {
            "type": "string"
        },
        "files": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string"
                    },
                    "content": {
                        "type": "string"
                    }
                },
                "required": ["path", "content"],
                "additionalProperties": False
            }
        }
    },
    "required": ["project_name", "description", "files"],
    "additionalProperties": False
}


SYSTEM_PROMPT = """
You are an expert software project code generator.

Convert the user's project idea into a complete beginner-friendly
software project.

IMPORTANT RULES:

1. Generate complete working code for every required file.
2. Do not use placeholder code.
3. Include all necessary HTML, CSS, JavaScript and configuration files.
4. Keep code simple and easy to understand.
5. Every file must have a relative path.
6. Every file must contain its complete source code as a string.
7. Never return file contents as separate text or Markdown.
8. Never return files as strings or arrays of strings.
9. Never generate passwords, API keys or secrets.
10. Never generate malware or destructive code.

OUTPUT FORMAT:

Return one JSON object with:
- project_name: a short project name using letters, numbers or hyphens.
- description: a short project description.
- files: an array of objects.

Every object inside files MUST contain:
- path: relative file path.
- content: complete file content as a string.

Example structure:

{
    "project_name": "snake-game",
    "description": "A simple snake game",
    "files": [
        {
            "path": "index.html",
            "content": "<html><body>Snake Game</body></html>"
        },
        {
            "path": "style.css",
            "content": "body { margin: 0; }"
        },
        {
            "path": "script.js",
            "content": "console.log('Snake Game');"
        }
    ]
}

Do not add explanations outside the JSON object.
"""


def clean_json_response(response_text: str) -> str:
    """Clean JSON response from the AI."""

    text = response_text.strip()

    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    return text.strip()


def generate_project(project_idea: str) -> dict:
    """Generate and validate project files using Ollama."""

    if not isinstance(project_idea, str) or not project_idea.strip():
        raise ValueError("Project idea cannot be empty.")

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": project_idea.strip()
            }
        ],
        format=PROJECT_SCHEMA,
        options={
            "temperature": 0.1,
            "num_predict": 6000,
            "num_ctx": 4096
        }
    )

    response_text = response.message.content or ""

    if not response_text.strip():
        raise ValueError("AI returned an empty response.")

    try:
        project_data = json.loads(
            clean_json_response(response_text)
        )
    except json.JSONDecodeError as error:
        raise ValueError(
            "AI returned invalid JSON. Please try again."
        ) from error

    if not isinstance(project_data, dict):
        raise ValueError("Invalid project response.")

    project_name = project_data.get("project_name")
    description = project_data.get("description")
    files = project_data.get("files")

    if not isinstance(project_name, str) or not project_name.strip():
        raise ValueError("AI did not generate a valid project name.")

    if not isinstance(description, str):
        raise ValueError("AI did not generate a valid description.")

    if not isinstance(files, list) or not files:
        raise ValueError("AI did not generate any project files.")

    if len(files) > 50:
        raise ValueError("AI generated too many files.")

    # Validate every generated file.
    for index, file_info in enumerate(files):

        if not isinstance(file_info, dict):
            raise ValueError(
                f"AI generated invalid file format at file number {index + 1}."
            )

        if not isinstance(file_info.get("path"), str):
            raise ValueError(
                f"Invalid file path at file number {index + 1}."
            )

        if not isinstance(file_info.get("content"), str):
            raise ValueError(
                f"Invalid file content at file number {index + 1}."
            )

        if not file_info["path"].strip():
            raise ValueError(
                f"Empty file path at file number {index + 1}."
            )

    return project_data
