# AI Voice Assistant Robot

An AI-powered Voice Assistant Robot built using Python, FastAPI, React.js, and local LLM technology.

## Features

- AI-powered chat using Ollama and Llama 3.2
- Voice input with Speech-to-Text
- Voice responses with Text-to-Speech
- Conversation history and memory
- Related follow-up questions
- Calculator tool integration
- Basic project and code file generation
- ZIP export of generated projects
- Interactive 3D robot interface

## Technologies Used

### Backend
- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL
- Pydantic Settings

### AI and Voice
- Ollama
- Llama 3.2
- Groq Speech-to-Text
- Edge TTS

### Frontend
- React.js
- Vite
- Three.js
- React Three Fiber
- React Three Drei
- React Markdown

## Project Structure

    AI-VOICE-ASSISTANT/
    |-- backend/
    |   |-- app/
    |   |   |-- agents/
    |   |   |-- api/
    |   |   |-- core/
    |   |   |-- database/
    |   |   |-- models/
    |   |   |-- project_builder/
    |   |   |-- schemas/
    |   |   |-- services/
    |   |   |-- tools/
    |   |-- requirements.txt
    |
    |-- frontend/
    |   |-- public/
    |   |-- src/
    |   |-- package.json
    |
    |-- voice_engine/
    |-- .gitignore
    |-- README.md

## Getting Started

### 1. Clone the Repository

    git clone YOUR_GITHUB_REPOSITORY_URL
    cd AI-VOICE-ASSISTANT

### 2. Backend Setup

    cd backend
    python -m venv .venv

Activate the virtual environment on Windows:

    .venv\Scripts\Activate.ps1

Install dependencies:

    pip install -r requirements.txt

Configure the required environment variables in a local .env file.

Make sure PostgreSQL and Ollama are installed and configured. Pull the Llama 3.2 model if it is not already available.

Start the backend:

    uvicorn app.main:app --reload --port 8002

### 3. Frontend Setup

Open another terminal:

    cd frontend
    npm install
    npm run dev

Open the local URL shown by Vite in your browser.

## Important Notes

- Configure API keys and database credentials locally.
- Never upload your .env file.
- PostgreSQL and Ollama must be running and configured.
- AI response quality and speed depend on the local model and hardware.
- Project generation provides basic code generation and validation.

## Future Improvements

- Improve AI response speed and accuracy.
- Add more AI tools and capabilities.
- Improve voice interaction.
- Enhance project generation and code validation.

## Author

Developed as a personal AI project to explore AI agents, LLM integration, voice technology, and full-stack development.
