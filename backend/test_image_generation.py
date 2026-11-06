import base64
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

print("Generating test image...")

result = client.images.generate(
    model="gpt-image-1",
    prompt="A colorful educational illustration of the solar system, with the Sun and eight planets clearly arranged in space.",
    size="1024x1024",
    quality="low"
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

output_path = Path("test_image.png")
output_path.write_bytes(image_bytes)

print(f"Image generated successfully: {output_path.resolve()}")
