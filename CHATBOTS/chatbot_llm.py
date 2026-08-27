from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import warnings

warnings.filterwarnings("ignore")

model_name = "HuggingFaceTB/SmolLM2-360M-Instruct"

print("Loading SmolLM2 model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.unk_token

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32
)
# Initialize conversation state with a system role
messages = [
    {
        "role": "system",
        "content": "You are a helpful, concise AI assistant. Answer in 2-3 lines."
    }
]

print("\nChatbot started. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.strip().lower() == "exit":
        print("Exiting chatbot.")
        break

    # 1. Append user input to conversation state
    messages.append({"role": "user", "content": user_input})

    # 2. Context Window: Retain system prompt + last 10 messages (5 turns)
    messages = [messages[0]] + messages[-10:]

    # 3. Format using ChatML template and tokenize
    tokenized = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
        return_dict=True,
        max_length=512
    )

    # 4. Generate response tokens with inference optimization
    with torch.inference_mode():
        outputs = model.generate(
            tokenized["input_ids"],
            attention_mask=tokenized["attention_mask"],
            max_new_tokens=60,
            temperature=0.5,
            top_p=0.8,
            do_sample=True,
            repetition_penalty=1.3,
            no_repeat_ngram_size=3,
            pad_token_id=tokenizer.pad_token_id
        )

    # 5. Slice prompt tokens away and decode generated IDs
    response = tokenizer.decode(
        outputs[0][tokenized["input_ids"].shape[-1]:],
        skip_special_tokens=True
    ).strip()

    print(f"Bot: {response}\n")

    # 6. Save assistant output to conversation state
    messages.append({"role": "assistant", "content": response})