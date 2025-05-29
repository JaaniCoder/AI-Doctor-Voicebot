from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import tempfile
import uuid
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from doctor import encode_image, analyze_image
from patient import transcription
from response import text_to_speech_with_elevenlabs, text_to_speech_with_gtts

app = FastAPI(title="AI Doctor Voice Bot API", version="1.0.0")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Add * for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# System prompt for the doctor
SYSTEM_PROMPT = """You have to act as a professional doctor specialist.
What's in the image? Do you find anything wrong with it medically?
If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in your
response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Do not say 'In the image I see' but say 'With what I see or notice, I think you have ....'
Do not respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot.
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please."""


@app.get("/api/health")
async def health_check():
    return {    
        "status": "healthy",
        }

if os.path.exists("dist"):
    app.mount("/", StaticFiles(directory="dist", html=True), name="static")

@app.post("/api/analyze")
async def analyze_medical_image(
    audio: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None)
):
    """
    Analyze medical image with voice input
    """

    try:
        # Check if GROQ API key is available
        if not os.environ.get("GROQ_API_KEY"):
            raise HTTPException(status_code=500, detail="GROQ API key not configured")
        
        # Create temporary directory for files
        temp_dir = tempfile.mkdtemp()
        session_id = str(uuid.uuid4())
        
        speech_text = ""
        doctor_response = ""
        audio_response_path = ""
        
        # Process audio if provided
        if audio:
            print(f"[INFO] Processing audio file: {audio.filename}")
            audio_path = os.path.join(temp_dir, f"audio_{session_id}.mp3")
            
            try:
                with open(audio_path, "wb") as f:
                    content = await audio.read()
                    f.write(content)
                
                print("[INFO] Transcribing audio...")
                speech_text = transcription(
                    GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
                    audio_filepath=audio_path,
                    stt_model="whisper-large-v3-turbo"
                )
                print(f"[INFO] Transcription successful: {speech_text[:50]}...")
                
            except Exception as e:
                print(f"[ERROR] Audio processing failed: {e}")
                speech_text = f"Audio processing failed: {str(e)}"
        
        # Process image if provided
        if image:
            print(f"[INFO] Processing image file: {image.filename}")
            image_path = os.path.join(temp_dir, f"image_{session_id}.jpg")
            
            try:
                with open(image_path, "wb") as f:
                    content = await image.read()
                    f.write(content)
                
                print("[INFO] Analyzing image...")
                query = SYSTEM_PROMPT + (speech_text if speech_text else "")
                encoded_image = encode_image(image_path)
                doctor_response = analyze_image(
                    query=query,
                    encoded_image=encoded_image,
                    model="meta-llama/llama-4-scout-17b-16e-instruct"
                )
                print(f"[INFO] Analysis successful: {doctor_response[:50]}...")
                
                # Generate audio response
                print("[INFO] Generating audio response...")
                audio_response_path = os.path.join(temp_dir, f"response_{session_id}.mp3")
                
                # Try ElevenLabs first, fallback to gTTS
                try:
                    text_to_speech_with_elevenlabs(doctor_response, audio_response_path)
                    print("[INFO] Audio generated with ElevenLabs")
                except Exception as e:
                    print(f"[WARNING] ElevenLabs failed: {e}. Using gTTS instead.")
                    text_to_speech_with_gtts(doctor_response, audio_response_path)
                    print("[INFO] Audio generated with gTTS")
                
            except Exception as e:
                print(f"[ERROR] Image processing failed: {e}")
                doctor_response = f"Image analysis failed: {str(e)}"
        else:
            doctor_response = "No image provided for analysis. Please upload a medical image for evaluation."
        
        return {
            "speech_to_text": speech_text,
            "doctor_response": doctor_response,
            "session_id": session_id,
            "has_audio_response": bool(audio_response_path and os.path.exists(audio_response_path)),
            "status": "success"
        }
    
    except Exception as e:
        print(f"[ERROR] Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/audio/{session_id}")
async def get_audio_response(session_id: str):
    """
    Get generated audio response
    """
    try:
        # Look for the audio file in temp directory
        import glob
        temp_dirs = [tempfile.gettempdir(), "/tmp", "./temp"]
        
        for temp_dir in temp_dirs:
            audio_path = os.path.join(temp_dir, f"response_{session_id}.mp3")
            if os.path.exists(audio_path):
                return FileResponse(
                    audio_path,
                    media_type="audio/mpeg",
                    filename=f"response_{session_id}.mp3"
                )
        
        # If not found, generate a simple fallback audio
        fallback_audio_path = f"fallback_{session_id}.mp3"
        text_to_speech_with_gtts("Audio response not found. Please try again.", fallback_audio_path)
        
        return FileResponse(
            fallback_audio_path,
            media_type="audio/mpeg",
            filename=f"fallback_{session_id}.mp3"
        )
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Audio file not found: {str(e)}")

@app.post("/text-to-speech")
async def convert_text_to_speech(text: str):
    """
    Convert text to speech
    """
    try:
        session_id = str(uuid.uuid4())
        temp_dir = tempfile.mkdtemp()
        audio_path = os.path.join(temp_dir, f"tts_{session_id}.mp3")
        
        # Try ElevenLabs first, fallback to gTTS
        try:
            text_to_speech_with_elevenlabs(text, audio_path)
        except Exception as e:
            print(f"ElevenLabs failed: {e}. Using gTTS.")
            text_to_speech_with_gtts(text, audio_path)
        
        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            filename=f"tts_{session_id}.mp3"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text-to-speech conversion failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)