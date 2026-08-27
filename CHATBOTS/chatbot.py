# Seq2Seq Chatbot (Encoder-Decoder Architecture with Sliding-Window History)
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# 1. Model Identifier
model_name = "facebook/blenderbot-400M-distill"

print("Loading model and tokenizer...")
# 2. Load Tokenizer & Model (downloads on first run, cached permanently after)
tokenizer = AutoTokenizer.from_pretrained(
    model_name, 
    local_files_only=True
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    model_name, 
    use_safetensors=False, 
    local_files_only=True
)

# 3. Initialize Conversation History List
conversation_history = []
print("\nChatbot ready! (type 'exit' to quit)\n")

# 4. Interactive Conversation Loop
while True:
    # Maintain a sliding context window (last 3 complete exchanges)
    conversation_history = conversation_history[-6:]
    
    # Serialize history list into a multiline string
    history_string = "\n".join(conversation_history)

    # Capture user input
    input_text = input("You: ")

    # Exit condition
    if input_text.strip().lower() == "exit":
        print("Goodbye!")
        break

    # Assemble structured prompt with completion cue
    prompt = history_string + f"\nUser: {input_text}\nBot:"

    # Tokenize input text to PyTorch tensors
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    # Generate output tokens via autoregressive sampling
    outputs = model.generate(
        **inputs,
        max_new_tokens=60,
        no_repeat_ngram_size=3,
        repetition_penalty=1.3,
        do_sample=True,
        temperature=0.6,
        top_p=0.85
    )

    # Decode token IDs into clean human-readable text
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    print(f"Bot: {response}\n")

    # Update conversation history state
    conversation_history.append(f"User: {input_text}")
    conversation_history.append(f"Bot: {response}")