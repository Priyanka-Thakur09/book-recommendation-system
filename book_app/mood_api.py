import requests
import random
import os

API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

mood_queries = {

    "happy": [
        "funny comedy books",
        "feel good novels",
        "uplifting fiction books",
        "light hearted books"
    ],

    "sad": [
        "emotional fiction books",
        "heart touching novels",
        "comfort books",
        "healing books"
    ],

    "romantic": [
        "best romance novels",
        "love story books",
        "romantic fiction",
        "contemporary romance novels"
    ],

    "thriller": [
        "psychological thriller books",
        "crime suspense novels",
        "mystery thriller books",
        "dark thriller fiction"
    ],

    "motivational": [
        "motivational self help books",
        "success mindset books",
        "productivity books",
        "personal growth books"
    ],

    "adventure": [
        "fantasy adventure novels",
        "epic fantasy books",
        "survival adventure books",
        "action adventure fiction"
    ]
}

def fetch_books_by_mood(mood):
   try:
       query = random.choice(mood_queries[mood])
  
       if not query:
             return []

       url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={API_KEY}"

       response = requests.get(url, timeout=10)

       data = response.json()

       books = []

       if 'items' not in data:
            return []

       for item in data['items'][:12]:

            volume = item.get('volumeInfo', {})

            books.append({

                "title": volume.get('title', 'Unknown'),

                "author": volume.get('authors', ['Unknown'])[0],

                "image": volume.get(
                    'imageLinks',
                    {}
                ).get(
                    'thumbnail',
                    ''
                ),

                "description": volume.get(
                    'description',
                    'No description available'
                )[:120]
            })

       return books

   except Exception as e:

        print("Mood API Error:", e)

        return []