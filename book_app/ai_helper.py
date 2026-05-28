from google import genai
import os

# 🔥 Gemini Client

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_ai(user_message):

    prompt = f"""
    You are a helpful AI book assistant.

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

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

    except Exception:
      return "AI service is temporarily unavailable."

    return response.text