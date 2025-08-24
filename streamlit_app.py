from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import streamlit as st

# ------------------ MODEL SETUP ------------------
@st.cache_resource
def load_model():
    base_model = AutoModelForCausalLM.from_pretrained(
        "tiiuae/falcon-7b",
        device_map="auto",
        torch_dtype=torch.bfloat16
    )
    model = PeftModel.from_pretrained(base_model, "Amod/falcon7b-mental-health-counseling")
    tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b")
    return model, tokenizer

model, tokenizer = load_model()

# ------------------ APP TITLE ------------------
st.title("Hi, I am Lada! ")
st.write("I'm your Mindfulness Buddy!")

# ------------------ CHAT HISTORY ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi I am Lada, your Mindfulness Buddy. I'm here to chat with you about how you're feeling and counsel you through any issue you're having. How are you feeling today?"
    })

# Restart button
if st.button("Start Over"):
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi I am Lada, your Mindfulness Buddy. I'm here to chat with you about how you're feeling and counsel you through any issue you're having. How are you feeling today?"
    })
    st.rerun()

# ------------------ PERSONALITY PROMPT ------------------
ai_instructions = """You are MindfulBuddy, a friendly AI that helps teenagers with their emotions.
- Be supportive, kind, and understanding
- Use language teenagers can understand
- If they ask for advice, provide simple, actionable suggestions
- If they mention wanting to hurt themselves or others, always tell them to calm down and encourage them to talk to a trusted adult immediately
- Suggest simple ways to feel better when appropriate (like deep breathing or talking to friends)
- Avoid complex jargon
- Keep responses short and friendly
"""

# ------------------ RESPONSE FUNCTION ------------------
def generate_response(prompt, history):
    # Add user input to history
    history.append({"role": "user", "content": prompt})

    # Turn history into conversation text
    conversation = "System: " + ai_instructions + "\n"
    for m in history:
        conversation += f"{m['role'].capitalize()}: {m['content']}\n"

    inputs = tokenizer(conversation, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    bot_reply = response.split("Assistant:")[-1].strip()

    history.append({"role": "assistant", "content": bot_reply})
    return bot_reply

# ------------------ CHAT UI ------------------
st.subheader("Chat with Lada")

# Display all messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle user input
if prompt := st.chat_input("Type here to chat with Lada..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = generate_response(prompt, st.session_state.messages)
            st.write(reply)
