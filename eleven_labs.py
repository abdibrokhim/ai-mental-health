from elevenlabs import clone, generate, play, set_api_key, VOICES_CACHE, voices
from elevenlabs.api import History
import os
from dotenv import load_dotenv




def with_premade_voice(prompt, voice, elevenlabs_api_key):
    
    load_dotenv()

    set_api_key(elevenlabs_api_key)
    
    audio_path = f'static/audio/{voice}.mp3'

    audio = generate(
        text=prompt,
        voice=voice,
        model="eleven_monolingual_v1"
    )

    # play(audio)

    try:
        with open(audio_path, 'wb') as f:
            f.write(audio)

        return audio_path
    
    except Exception as e:
        print(e)

        return ""

