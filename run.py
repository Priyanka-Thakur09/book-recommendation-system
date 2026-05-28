from dotenv import load_dotenv
load_dotenv()

from book_app import create_app
from book_app.dbmodels import db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

print(app.static_folder)