
import os
import shutil
import tempfile
import base64
import time
import logging

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
    Depends
)
from fastapi.responses import Response
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool
from pydantic import BaseModel

from app.database.connection import get_db
from app.schemas.chat import ChatRequest
from app.api.chat import chat as process_chat
from app.services.speech_to_text import transcribe_audio
from app.services.text_to_speech import generate_speech

router = APIRouter(prefix="/voice", tags=["Voice"])

logger = logging.getLogger(__name__)


class SpeakRequest(BaseModel):
    text: str


# 1. Text to Speech API
@router.post("/speak")
async def speak_text(request: SpeakRequest):
    try:
        start_time = time.perf_counter()

        audio_data = await generate_speech(request.text)

        tts_time = time.perf_counter() - start_time

        logger.info(
            "TTS processing time: %.2f seconds",
            tts_time
        )

        return Response(
            content=audio_data,
            media_type="audio/mpeg"
        )

    except Exception as error:
        logger.exception("Speech generation failed")

        raise HTTPException(
            status_code=500,
            detail=f"Speech generation failed: {str(error)}"
        )


# 2. Speech to Text API
@router.post("/transcribe")
async def transcribe_voice(file: UploadFile = File(...)):

    allowed_extensions = {
        ".wav", ".mp3", ".m4a", ".webm", ".ogg"
    }

    extension = os.path.splitext(
        file.filename or ""
    )[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format"
        )

    temp_path = None

    try:
        start_time = time.perf_counter()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name

        result = await run_in_threadpool(
            transcribe_audio,
            temp_path
        )

        total_time = time.perf_counter() - start_time

        logger.info(
            "Transcription processing time: %.2f seconds",
            total_time
        )

        return {
            "message": "Audio transcribed successfully",
            "text": result["text"],
            "language": result["language"],
            "processing_time": round(total_time, 2)
        }

    except HTTPException:
        raise

    except Exception as error:
        logger.exception("Transcription failed")

        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(error)}"
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

        await file.close()


# 3. Complete Voice Assistant API
@router.post("/ask")
async def ask_voice(
    conversation_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    allowed_extensions = {
        ".wav", ".mp3", ".m4a", ".webm", ".ogg"
    }

    extension = os.path.splitext(
        file.filename or ""
    )[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format"
        )

    temp_path = None

    request_start = time.perf_counter()

    timings = {}

    try:
        # Step 1: Save uploaded audio
        stage_start = time.perf_counter()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name

        timings["upload_save"] = round(
            time.perf_counter() - stage_start, 2
        )

        # Step 2: Speech to Text - Groq Whisper
        stage_start = time.perf_counter()

        transcription = await run_in_threadpool(
            transcribe_audio,
            temp_path
        )

        user_message = transcription["text"].strip()

        timings["whisper"] = round(
            time.perf_counter() - stage_start, 2
        )

        if not user_message:
            raise HTTPException(
                status_code=400,
                detail="No speech detected"
            )

        # Step 3: AI Brain - Ollama + Memory
        stage_start = time.perf_counter()

        chat_result = await run_in_threadpool(
            process_chat,
            ChatRequest(
                conversation_id=conversation_id,
                message=user_message
            ),
            db
        )

        # FIX: ChatResponse is a Pydantic object,
        # so access its fields using dot notation.
        ai_response = chat_result.response

        related_questions = chat_result.related_questions

        timings["llm"] = round(
            time.perf_counter() - stage_start, 2
        )

        # Step 4: Text to Speech - Edge TTS
        stage_start = time.perf_counter()

        audio_data = await generate_speech(ai_response)

        timings["tts"] = round(
            time.perf_counter() - stage_start, 2
        )

        # Step 5: Total processing time
        timings["total"] = round(
            time.perf_counter() - request_start, 2
        )

        logger.info(
            "Voice processing timings: %s",
            timings
        )

        # Step 6: Return response
        return {
            "transcribed_text": user_message,
            "response": ai_response,
            "related_questions": related_questions,
            "audio_base64": base64.b64encode(
                audio_data
            ).decode("utf-8"),
            "language": transcription["language"],
            "timings": timings
        }

    except HTTPException:
        raise

    except Exception as error:
        logger.exception("Voice assistant failed")

        raise HTTPException(
            status_code=500,
            detail=f"Voice assistant failed: {str(error)}"
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

        await file.close()
