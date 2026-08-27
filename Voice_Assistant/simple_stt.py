import os
from dotenv import load_dotenv
from groq import Groq

# 1. Load environment variables (.env)
load_dotenv()

# 2. Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 3. Path to your recorded voice file (must be in the same folder)
audio_path = "my_audio.m4a"  # <-- Put your exact recorded filename here (.mp3, .wav, .m4a)

# 4. Open and transcribe
with open(audio_path, "rb") as f:
    transcription = client.audio.transcriptions.create(
        file=(os.path.basename(audio_path), f.read()),
        model="whisper-large-v3-turbo",
        response_format="text"
    )

# 5. Print the output
print("\n--- Transcription Output ---")
print(transcription)