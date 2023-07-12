from flask import Flask, jsonify, request
from datamanager.json_data_manager import JSONDataManager
import requests

API_KEY = "24808d93"
app = Flask(__name__)
data_manager = JSONDataManager('movies.json')  # Use the appropriate path to your JSON file


def request_info_movie_api(title):
    """Obtains the information of the movie requests
    if the movie is available in the API"""
    movie_info = requests.get(f"http://www.omdbapi.com/",
                              params={"apikey": API_KEY, "t": title}).json()
    if 'Error' in movie_info:
        if movie_info['Error'] == 'Invalid API key!':
            raise Exception("Invalid API Key")
        if movie_info['Error'] == 'Movie not found!':
            raise Exception("The movie was not found")
    return movie_info["Title"], movie_info["Year"], movie_info["imdbRating"], movie_info["Poster"], \
        movie_info['Director']


@app.route("/")
def home():
    return jsonify("Welcome to the web app")


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return str(users)  # Temporarily returning users as a string


@app.route("/users/<user_id>")
def users_movies(user_id):
    list_of_movies_data = data_manager.get_user_movies(user_id)
    return str(list_of_movies_data)


@app.route("/add_user", methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        data_manager.add_user(request.form.get('name'))
        return 'User added'
    else:
        pass


@app.route("/users/<user_id>/add_movie", methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        data_manager.add_user_movie(user_id, request_info_movie_api(request.form.get('name')))
        return 'Movie added'
    else:
        pass


@app.route("/users/<user_id>/update_movie/<int:movie_id>", methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        data_manager.update_user_movie(user_id, movie_id, request.json)
        return 'Movie updated'
    else:
        pass


@app.route("/users/<user_id>/delete_movie/<int:movie_id>", methods=['GET', 'POST'])
def delete_movie(user_id, movie_id):
    if request.method == 'POST':
        data_manager.delete_user_movie(user_id, movie_id)
        return f'Movie {movie_id} deleted for user {user_id}'
    else:
        pass


if __name__ == '__main__':
    app.run(debug=True)
