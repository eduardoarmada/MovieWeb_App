from flask import Flask
from datamanager.json_data_manager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('movies.json')  # Use the appropriate path to your JSON file


@app.route("/")
def home():
    return "hello world"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return str(users)  # Temporarily returning users as a string


@app.route("/users/<user_id>")
def users_movies():
    return "hello world"


@app.route("/add_user")
def add_user():
    return "hello world"


@app.route("/users/<user_id>/add_movie")
def add_movie():
    return "hello world"


@app.route("/users/<user_id>/update_movie/<movie_id>")
def update_movie():
    return "hello world"


@app.route("/users/<user_id>/update_movie/<movie_id>")
def delete_movie():
    return "hello world"


if __name__ == '__main__':
    app.run(debug=True)
