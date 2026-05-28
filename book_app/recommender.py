import pickle
import numpy as np

popular_df = pickle.load(open('model/popular.pkl','rb'))
pt = pickle.load(open('model/pt.pkl','rb'))
books = pickle.load(open('model/books.pkl','rb'))
similarity_scores = pickle.load(open('model/similarity_scores.pkl','rb'))

def get_popular_books():
    return popular_df


def recommend_books(user_input):
    if user_input not in pt.index:
        return None

    index = np.where(pt.index == user_input)[0][0]

    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:5]

    data = []

    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]

        item = [
            temp_df['Book-Title'].values[0],
            temp_df['Book-Author'].values[0],
            temp_df['Image-URL-M'].values[0]
        ]

        data.append(item)

    return data

#for automatic suggestions
def get_book_titles():
    return list(pt.index.values)