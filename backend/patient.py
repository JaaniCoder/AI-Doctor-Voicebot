# Setting Audio Recorder

import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from groq import Groq


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Simplified function to record audio from the microphone and save it as an mp3 file.
    
    Args:
    file_path(str): Path to save the recorded audio file.
    timeout(int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit(int): Maximum time for the phrase to be recorded (in seconds).
    """

    recogniser = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recogniser.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now....")

            # Recording the audio

            audio_data = recogniser.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            # Convert the recorded audio to an mp3 file
            
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format='mp3', bitrate='128k')

            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

audio_filepath = "patient_voice_test.mp3"
record_audio(file_path=audio_filepath)


# Setting up Speech-To-Text (STT) model for transcription

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
stt_model = "whisper-large-v3-turbo"

def transcription(stt_model, audio_filepath, GROQ_API_KEY):
    client = Groq(api_key=GROQ_API_KEY)
    audio_file = open(audio_filepath, "rb")

    transcription = client.audio.transcriptions.create(
        model=stt_model,
        file=audio_file,
        language="en"
    )

    return transcription.text