import streamlit as st
from openai import OpenAI

OPENAI_API_KEY="..."

# Title and description
st.title("Hi, I am Lada! ")
st.write("I'm your Mindfulness Buddy!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Start conversation with a default message if just started
if len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi I am Lada, your Mindfulness Buddy. I'm here to chat with you about how you're feeling and counsel you through any issue they're having. How are you feeling today?"
    })

# Restart button
if st.button("Start Over"):
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi I am Lada, you Mindfulness Buddy. I'm here to chat with you about how you're feeling and counsel you through any issue they're having. How are you feeling today?"
    })
    st.rerun()

# Display all messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle user input
if prompt := st.chat_input("Type here to chat with MindfulBuddy..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Define assistant behavior and personality
    ai_instructions = """You are MindfulBuddy, a friendly AI that helps teenagers with their emotions.
    - Be supportive, kind, and understanding
    - Use language teenagers can understand
    - If they ask for advice, provide simple, actionable suggestions
    - If they metion wanting to hurt themselves or others, always tell them to calm down and think about it, and encourage them to talk to a trusted adult immediately
    - Suggest simple ways to feel better when appropriate (like deep breathing or talking to friends)
    - Avoid complex jargon or overly technical terms
    - Always suggest that they can talk to you about anything
    - If they mention feeling sad, anxious, or stressed, tell them it's okay to feel that way and encourage to talk about it
    - If they mention feeling happy, encourage them and celebrate their happiness
    - If they mention feeling angry, suggest ways to calm down like taking deep breaths or counting
    - NEVER give medical advice or diagnose conditions
    - If someone mentions harming themselves or others, always encourage them to talk to a trusted adult immediately
    - Keep responses fairly short and friendly
    - Use slang and casual language when appropriate, but always be respectful
    """

    # Compile messages for OpenAI
    messages_for_ai = [{"role": "system", "content": ai_instructions}] + st.session_state.messages

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                client = OpenAI(api_key=MY_API_KEY)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages_for_ai,
                    temperature=0.7,
                    max_tokens=75,
                )
                buddy_response = response.choices[0].message.content
                st.write(buddy_response)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": buddy_response
                })
    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")
