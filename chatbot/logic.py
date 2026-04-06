from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def get_response(user_input, personality="Friendly", model="DialoGPT-small"):
    # Load model dynamically
    tokenizer = AutoTokenizer.from_pretrained(f"microsoft/{model}")
    model_instance = AutoModelForCausalLM.from_pretrained(f"microsoft/{model}")

    # Generate response
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    chat_history_ids = model_instance.generate(
        new_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(chat_history_ids[:, new_input_ids.shape[-1]:][0], skip_special_tokens=True)

    # Adjust personality
    if personality == "Friendly":
        response = "😊 " + response
    elif personality == "Professional":
        response = "📊 " + response
    elif personality == "Funny":
        response = "😂 " + response

    return response
