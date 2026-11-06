import edge_tts


async def generate_speech(
    text: str,
    voice: str = "hi-IN-SwaraNeural"
) -> bytes:

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice
    )

    audio_data = bytearray()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])

    if not audio_data:
        raise RuntimeError("Speech audio generation failed")

    return bytes(audio_data)