import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_meeting(transcript_text):
    prompt = f"""
You are an expert executive meeting assistant.
Analyze the following transcript (ignore any audio glitches or repeated words):

<Transcript>
{transcript_text}
</Transcript>

Please provide a clear, structured summary in English:
1. **Executive Summary** (2-3 sentences)
2. **Key Discussion Points** (bullet points)
3. **Core Conclusion & Need for AI**
"""
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip()

# --- Test block ---
if __name__ == "__main__":
    sample_urdu_transcript = (
        "تو میری اس میٹنگ کا مقصد یہ ہے کہ آپ کو اچھی طرح یہ بتا سکیں کہ اس دنیا میں جو تبدیلیاں آ رہی ہیں "
        "وہ زیادہ سے زیادہ کس وجہ سے ہیں۔ جنریٹو اے آئی کی وجہ سے ہیں یا ہونے والے نئے اقدامات کی وجہ سے۔ "
        "ہر جگہ اے آئی کا چرچا ہے، انڈسٹری بوم کر رہی ہے، بزنس کو اے آئی کی ضرورت ہے۔"
    )
    print(summarize_meeting(sample_urdu_transcript))