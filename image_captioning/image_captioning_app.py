import gradio as gr
import numpy as np
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# 1. Load Processor and Model from local cache
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base", 
    use_safetensors=False
)

def caption_image(image):
    # Guard against empty/cleared upload
    if image is None:
        return ""
    
    # Convert numpy array to PIL RGB
    raw_img = Image.fromarray(image).convert('RGB')
    
    # Prepare tensors
    text = "a photography of"
    inputs = processor(raw_img, text, return_tensors="pt")
    
    # Generate tokens (single pass)
    output = model.generate(**inputs, max_length=50)
    
    # Decode to text
    final_output = processor.decode(output[0], skip_special_tokens=True)
    return final_output

# 2. Build and launch UI
gr.Interface(
    fn=caption_image,
    inputs=gr.Image(type="numpy"),
    outputs="text",
    title="Image Captioning with BLIP",
    description="Upload an image to generate a caption."
).launch()