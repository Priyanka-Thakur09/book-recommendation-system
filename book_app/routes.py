from flask import Blueprint, render_template, request
from .recommender import get_popular_books, recommend_books, get_book_titles
from flask_login import login_required
from .mood_api import fetch_books_by_mood
from .ai_helper import ask_ai
from flask import jsonify

main = Blueprint('main', __name__)

@main.route('/')
def index():
    popular_df = get_popular_books()
    
    return render_template(
        'index.html',
        book_name=list(popular_df['Book-Title'].values),
        author=list(popular_df['Book-Author'].values),
        image=list(popular_df['Image-URL-M'].values),
        votes=list(popular_df['num_ratings'].values),
        rating=list(popular_df['avg_rating'].values)
    )


@main.route('/recommend')
@login_required
def recommend_ui():
    book_list = get_book_titles()
    return render_template('recommend.html', book_list=book_list)


@main.route('/recommend_books', methods=['POST'])
@login_required
def recommend():

    user_input = request.form.get('user_input')

    data = recommend_books(user_input)

    # HANDLE BOOK NOT FOUND

    if not data:

        return render_template(
            'recommend.html',
            error="Book not found in database.",
            book_list=get_book_titles()
        )

    return render_template(
        'recommend.html',
        data=data,
        book_list=get_book_titles()
    )


@main.route('/moods')
def moods():
    return render_template('moods.html')


@main.route('/mood/<mood_name>')
def mood_result(mood_name):

    books = fetch_books_by_mood(mood_name)

    if not books:

        return render_template(
            'mood_result.html',
            error="Unable to fetch books right now. Please try again.",
            mood=mood_name.capitalize()
        )

    return render_template(
        'mood_result.html',
        books=books,
        mood=mood_name.capitalize()
    )

'''
@main.route('/chatbot', methods=['GET', 'POST'])
@login_required
def chatbot():

    ai_response = None

    error = None

    user_message = None

    

    if request.method == 'POST':

        user_message = request.form.get('message')
        print("USER MESSAGE:", user_message)

        try:

            ai_response = ask_ai(user_message)
            print("AI RESPONSE:", ai_response)

        except Exception as e:

            error = str(e)
            print("ERROR:", error)

    return render_template(

        'chatbot.html',

        ai_response=ai_response,

        user_message=user_message,

        error=error,

        books=None
    )
'''
@main.route('/chatbot')
@login_required
def chatbot():
    return render_template('chatbot.html')


@main.route('/chatbot_api', methods=['POST'])
@login_required
def chatbot_api():
    data = request.get_json()
    user_message = data.get('message')

    try:

        ai_response = ask_ai(user_message)

        return jsonify({
            "response": ai_response
        })

    except Exception as e:

        return jsonify({
            "response": f"Error: {str(e)}"
        })