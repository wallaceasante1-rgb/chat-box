from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Global variables
tokenizer = None
model_instance = None
chat_history_ids = None

def load_model(model_name="DialoGPT-small"):
    global tokenizer, model_instance
    tokenizer = AutoTokenizer.from_pretrained(f"microsoft/{model_name}")
    model_instance = AutoModelForCausalLM.from_pretrained(f"microsoft/{model_name}")

# Load default model at startup
load_model()

def get_response(user_input, personality="Friendly", model="DialoGPT-small"):
    global chat_history_ids, tokenizer, model_instance

    # Reload model if user switches
    if tokenizer is None or model_instance is None or f"microsoft/{model}" != model_instance.config._name_or_path:
        load_model(model)

    # Encode user input
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Append to history if exists
    if chat_history_ids is not None:
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
    else:
        bot_input_ids = new_input_ids

    # Generate response
    chat_history_ids = model_instance.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id
    )

    response = tokenizer.decode(
        chat_history_ids[:, bot_input_ids.shape[-1]:][0],
        skip_special_tokens=True
    )

    # Personality tweak
    if personality == "Friendly":
        response = "😊 " + response
    elif personality == "Professional":
        response = "📊 " + response
    elif personality == "Funny":
        response = "😂 " + response

    return response

def reset_chat():
    global chat_history_ids
    chat_history_ids = None

