from flask import Flask, jsonify, request, render_template
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
    data = data_manager.get_all_data()
    return render_template("users_list.html", users=data)


@app.route("/users/<user_id>")
def users_movies(user_id):
    list_of_movies_data = data_manager.get_user_movies(user_id)
    return render_template('users_movie.html', users_id=user_id, movies=list_of_movies_data)


@app.route("/add_user", methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        data_manager.add_user(request.form.get('name'))
        data = data_manager.get_all_data()
        return render_template("users_list.html", users=data)
    else:
        return render_template('add_user.html')


@app.route("/users/<user_id>/add_movie", methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        data_manager.add_user_movie(user_id, request_info_movie_api(request.form.get('name')))
        list_of_movies_data = data_manager.get_user_movies(user_id)
        return render_template('users_movie.html', users_id=user_id, movies=list_of_movies_data)
    else:
        return render_template('add_movie.html', user_id=user_id)


@app.route("/users/<user_id>/update_movie/<int:movie_id>", methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        data_manager.update_user_movie(user_id, movie_id, request.form)
        list_of_movies_data = data_manager.get_user_movies(user_id)
        return render_template('users_movie.html', users_id=user_id, movies=list_of_movies_data)
    else:
        return render_template('update_movie.html', user_id=user_id, movie_id=movie_id)


@app.route("/users/<user_id>/delete_movie/<int:movie_id>", methods=['GET', 'POST'])
def delete_movie(user_id, movie_id):
    if request.method == 'POST':
        data_manager.delete_user_movie(user_id, movie_id)
        list_of_movies_data = data_manager.get_user_movies(user_id)
        return render_template('users_movie.html', users_id=user_id, movies=list_of_movies_data)
    else:
        return render_template('delete_movie.html', user_id=user_id, movie_id=movie_id)


if __name__ == '__main__':
    app.run(debug=True)
