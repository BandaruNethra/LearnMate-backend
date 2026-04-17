import os
from groq import Groq
from dotenv import load_dotenv

# 1. Load the variables from your .env file
# Explicitly tell it to look in the current directory
load_dotenv()

# 2. Get the key and check it
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    # This prevents the crash. It will print a warning instead.
    print("❌ BACKEND ERROR: GROQ_API_KEY is missing from .env")
    client = None
else:
    client = Groq(api_key=api_key)

def generate_learning_response(user_message, context_data=""):
    video_vault = {
        "python": "https://www.youtube.com/embed/kqtD5dpn9C8",
        "javascript": "https://www.youtube.com/embed/W6NZfCO5SIk",
        "java": "https://www.youtube.com/embed/eIrMbAQSU34",
        "cpp": "https://www.youtube.com/embed/vLnPwxZdW4Y",
        "html": "https://www.youtube.com/embed/ok-plXXHlWw"
    }

    # Identify the topic
    topic = "python" # default
    for key in video_vault:
        if key in user_message.lower():
            topic = key

    video_url = video_vault.get(topic, "https://www.youtube.com/embed/kqtD5dpn9C8")

    # The Sassy Tutor Prompt
    system_prompt = (
        f"You are LearnMate AI (Grok edition). The user's focus is {context_data}. "
        "Be witty, detailed, and slightly sarcastic. "
        "If they ask for basics, include this EXACT line at the end of your response: "
        f"VIDEO_LINK: {video_url}"
    )
    
    if client is None:
        return "Backend Error: Please set GROQ_API_KEY in the backend/.env file."
    
    try:
        completion = client.chat.completions.create(
            # Using the fast versatile model
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"