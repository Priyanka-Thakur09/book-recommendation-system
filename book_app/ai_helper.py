from google import genai
import os

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
def ask_ai(user_message):
    prompt = f"""
    You are a helpful AI book assistant.
    You are an expert AI Book Assistant.

    Rules:
    - Never invent book titles, authors, publication years, publishers, plots, or characters.
    - If you are not certain about a fact, say:
    "I'm not sure. I don't have reliable information about that book."
    - If the user provides the author name, use it.
    - If a book title is ambiguous, ask the user to specify the author instead of guessing.
    - Keep responses concise and accurate.
    
    User query:
    {user_message}

    Give short, useful responses about books.
    """
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

    except Exception:
      try:  
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

      except Exception:
         return "AI service is temporarily unavailable."

    return response.text