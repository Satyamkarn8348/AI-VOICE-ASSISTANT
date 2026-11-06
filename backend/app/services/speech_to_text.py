
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)


def transcribe_audio(file_path: str) -> dict:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing in .env file")

    client = Groq(api_key=api_key)

    prompt = (
        "This is Hindi and Hinglish speech about software development. "
        "Keep technical terms in English exactly as written: "
        "Java, Python, React, Spring Boot, JavaScript, SQL, API, and coding. "
        "If the speaker says Java, write Java, not जाबा or जावा."
    )

    with open(file_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            file=(Path(file_path).name, audio_file),
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
            language="hi",
            prompt=prompt,
            temperature=0
        )

    return {
        "text": result.text,
        "language": getattr(result, "language", "unknown")
    }
