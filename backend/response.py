# Setting up Text-to-Speech (TTS) model with gTTS and ElevenLabs

import os
import elevenlabs
from elevenlabs.client import ElevenLabs
from gtts import gTTS
import subprocess
import platform

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    if not ELEVENLABS_API_KEY:
        print("Warning: ElevenLabs API key not found. Using gTTS instead.")
        return text_to_speech_with_gtts(input_text, output_filepath)
    
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        voice_id = "FGY2WhTYpPnrIDTdsKH5"

        audio = client.text_to_speech.convert(
            text=input_text,
            voice_id=voice_id,
            output_format='mp3_22050_32',
            model_id='eleven_turbo_v2'
        )
        elevenlabs.save(audio, output_filepath)
    except Exception as e:
        print(f"ElevenLabs error: {e}. Falling back to gTTS.")
        return text_to_speech_with_gtts(input_text, output_filepath)

def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)

    os_name = platform.system()

    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # windows
            subprocess.run(['powershell', '-c', f'(Start-Process -FilePath "{output_filepath}")'])
        elif os_name == "Linux":  # linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """
    Convert text to speech using ElevenLabs API with fallback to gTTS
    """
    if not ELEVENLABS_API_KEY:
        print("Warning: ElevenLabs API key not found. Using gTTS instead.")
        return text_to_speech_with_gtts(input_text, output_filepath)
    
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        voice_id = "FGY2WhTYpPnrIDTdsKH5"

        audio = client.text_to_speech.convert(
            text=input_text,
            voice_id=voice_id,
            output_format='mp3_22050_32',
            model_id='eleven_turbo_v2'
        )
        elevenlabs.save(audio, output_filepath)
        print("Audio generated successfully with ElevenLabs")
        
        # Play audio
        os_name = platform.system()
        try:
            if os_name == "Darwin":  # macOS
                subprocess.run(['afplay', output_filepath])
            elif os_name == "Windows":  # windows
                subprocess.run(['powershell', '-c', f'(Start-Process -FilePath "{output_filepath}")'])
            elif os_name == "Linux":  # linux
                subprocess.run(['aplay', output_filepath])
            else:
                raise OSError("Unsupported operating system")
        except Exception as e:
            print(f"An error occurred while trying to play the audio: {e}")
            
    except Exception as e:
        print(f"ElevenLabs error: {e}. Falling back to gTTS.")
        return text_to_speech_with_gtts(input_text, output_filepath)

# Remove the automatic execution that was causing issues
# Only run test code if this file is executed directly
if __name__ == "__main__":
    input_text = "Hi this is JaaniCoder! Testing the TTS system."
    print("Testing gTTS...")
    text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing.mp3")
    
    print("Testing ElevenLabs...")
    text_to_speech_with_elevenlabs(input_text=input_text, output_filepath="elevenlabs_testing.mp3")