import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# 1. Load Processor and Model from local cache (using your downloaded .bin weights)
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base", 
    use_safetensors=False
)

# 2. Path to your image
image_path = "test.jpg"

if not os.path.exists(image_path):
    print(f"Error: Could not find '{image_path}'. Place an image named '{image_path}' in this folder.")
else:
    # 3. Load & convert to RGB
    raw_img = Image.open(image_path).convert('RGB')

    # 4. Prepare inputs (image + prompt)
    text = "a photography of"
    inputs = processor(raw_img, text, return_tensors="pt")

    # 5. Generate tokens
    output = model.generate(**inputs, max_length=50)

    # 6. Decode output tokens to text
    final_output = processor.decode(output[0], skip_special_tokens=True)
    print("Generated Caption:", final_output)