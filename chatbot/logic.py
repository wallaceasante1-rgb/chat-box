from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model once
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

chat_history_ids = None

def get_response(user_input, personality="Friendly", model_choice="DialoGPT-small"):
    global chat_history_ids

    # Load model dynamically if user switches
    tokenizer_local = AutoTokenizer.from_pretrained(f"microsoft/{model_choice}")
    model_local = AutoModelForCausalLM.from_pretrained(f"microsoft/{model_choice}")

    # Encode input
    new_input_ids = tokenizer_local.encode(user_input + tokenizer_local.eos_token, return_tensors='pt')

    if chat_history_ids is not None:
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
    else:
        bot_input_ids = new_input_ids

    chat_history_ids = model_local.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer_local.eos_token_id
    )

    response = tokenizer_local.decode(
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
def get_response(user_input, personality="Friendly", model_choice="DialoGPT-small"):
    # For now, just return a simple response so the app runs
    response = f"Bot ({personality}, {model_choice}) reply to: {user_input}"
    return response

def reset_chat():
    # Placeholder reset function
    pass
