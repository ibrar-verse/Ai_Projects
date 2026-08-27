import os
from dotenv import load_dotenv
import gradio as gr
from groq import Groq
from google import genai

# 1. Load API Keys from .env
load_dotenv()

GROQ_KEY = os.getenv("GROQ_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# 2. Initialize Cloud Clients
groq_client = Groq(api_key=GROQ_KEY)
gemini_client = genai.Client(api_key=GEMINI_KEY)


# 3. Cloud Whisper Speech-to-Text
def transcribe_audio(audio_path):
    if not audio_path:
        return "No audio file provided. Please record or upload an audio clip."

    try:
        with open(audio_path, "rb") as file_data:
            transcription = groq_client.audio.transcriptions.create(
                file=(os.path.basename(audio_path), file_data.read()),
                model="whisper-large-v3-turbo",
                response_format="text"
            )
        return transcription.strip()
    except Exception as e:
        return f"Whisper Transcription Error: {str(e)}"


# 4. Gemini Meeting Summarizer
def summarize_meeting(transcript_text):
    if not transcript_text or transcript_text.startswith("Whisper Transcription Error") or transcript_text.startswith("No audio"):
        return "⚠️ *Cannot generate summary without a valid transcript.*"

    prompt = f"""
You are an expert executive meeting assistant.
Analyze the following transcript (which may be in English, Urdu, or mixed languages, and might contain audio glitch repetitions):

<Transcript>
{transcript_text}
</Transcript>

Please provide a clean, professional, and well-structured meeting summary in English:
1. **Executive Summary** (2-3 sentences explaining the core objective)
2. **Key Discussion Points** (bullet points highlighting the main ideas)
3. **Decisions Made & Action Items** (any takeaways, next steps, or conclusions)
"""
    try:
        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Gemini Summarization Error: {str(e)}"


# 5. Full End-to-End Pipeline
def process_meeting(audio_file):
    # Step A: Cloud Whisper STT
    transcript = transcribe_audio(audio_file)
    
    # Step B: Gemini Summarization
    summary = summarize_meeting(transcript)
    
    return transcript, summary


# 6. Gradio UI
with gr.Blocks(title="AI Business Meeting Companion") as demo:
    gr.Markdown("# 🎙️ AI Business Meeting Companion")
    gr.Markdown(
        "Record your voice or upload a meeting recording (`.mp3`, `.wav`, `.m4a`). "
        "Audio is transcribed via **Cloud Whisper** and analyzed into structured meeting minutes using **Gemini Flash**."
    )

    with gr.Row():
        audio_input = gr.Audio(
            sources=["upload", "microphone"],
            type="filepath",
            label="Upload or Record Meeting Audio"
        )

    submit_btn = gr.Button("Analyze Meeting", variant="primary")

    with gr.Row():
        transcript_box = gr.Textbox(
            label="Raw Speech Transcript (Whisper)",
            lines=8,
            placeholder="Transcribed text will appear here..."
        )
        summary_box = gr.Markdown(
            label="Executive Meeting Summary",
            value="*Meeting minutes and key takeaways will be displayed here.*"
        )

    # Trigger pipeline on button click
    submit_btn.click(
        fn=process_meeting,
        inputs=[audio_input],
        outputs=[transcript_box, summary_box]
    )

if __name__ == "__main__":
    demo.launch()