from flask import Flask, jsonify, request, render_template
from datamanager.json_data_manager import JSONDataManager
import requests
import os
from datamanager.SQLiteDataManager import data_manager as dm, Movie, User


API_KEY = "24808d93"

app = Flask(__name__)
#data_manager = JSONDataManager('movies.json')  # Use the appropriate path to your JSON file

file_path = os.path.abspath(os.getcwd())+"/data/movies.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path

data_manager = dm
data_manager.create_app(app)


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
    """Endpoint to the index page of the application"""
    return render_template('index.html')


@app.route('/users')
def list_users():
    """Endpoint to the display of all the users available in the database"""
    data = data_manager.get_all_data()
    return render_template("users_list.html", users=data)


@app.route("/users/<user_id>")
def users_movies(user_id):
    """Endpoint to the display of all the movies available of the user selected"""
    try:
        list_of_movies_data = data_manager.get_user_movies(user_id)

    except IOError as e:
        return render_template("400.html", error_message=str(e)), 400

    return render_template('users_movie.html', users_id=user_id, movies=list_of_movies_data)


@app.route("/add_user", methods=['GET', 'POST'])
def add_user():
    """Endpoint to add a user in the database"""
    if request.method == 'POST':
        if request.form.get('name') is None:
            return render_template("400.html", error_message="No name was introduced"), 400

        data_manager.add_user(request.form.get('name'))
        data = data_manager.get_all_data()
        return render_template("users_list.html", users=data)

    else:
        return render_template('add_user.html')


@app.route("/users/<user_id>/add_movie", methods=['GET', 'POST'])
def add_movie(user_id):
    """Endpoint to add a movie to the selected user in the database"""
    if int(user_id) not in data_manager.get_all_data():
        return render_template("400.html", error_message="No user with that ID was found"), 400

    if request.method == 'POST':
        if request.form.get("name") is None:
            return render_template("400.html", error_message="No name of movie was introduced"), 400

        data_manager.add_user_movie(user_id, request_info_movie_api(request.form.get('name')))
        list_of_movies_data = data_manager.get_user_movies(user_id)
        return render_template('users_movie.html', users_id=user_id, movies=list_of_movies_data)

    else:
        return render_template('add_movie.html', user_id=user_id)


@app.route("/users/<user_id>/update_movie/<int:movie_id>", methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """Endpoint to update the selected movie data"""
    if int(user_id) not in data_manager.get_all_data():
        return render_template("400.html", error_message="No user with that ID was found"), 400

    if request.method == 'POST':
        if movie_id not in [movie['id'] for movie in data_manager.get_user_movies(user_id)]:
            return render_template("400.html", error_message="No movie was found with that ID"), 400

        data_manager.update_user_movie(user_id, movie_id, request.form)
        list_of_movies_data = data_manager.get_user_movies(user_id)
        return render_template('users_movie.html', users_id=user_id, movies=list_of_movies_data)

    else:
        return render_template('update_movie.html', user_id=user_id, movie_id=movie_id)


@app.route("/users/<user_id>/delete_movie/<int:movie_id>", methods=['GET', 'POST'])
def delete_movie(user_id, movie_id):
    """Endpoint to delete the movie of the user's movies"""
    if int(user_id) not in data_manager.get_all_data():
        return render_template("400.html", error_message="No user with that ID was found"), 400

    if request.method == 'POST':
        data_manager.delete_user_movie(user_id, movie_id)
        list_of_movies_data = data_manager.get_user_movies(user_id)
        return render_template('users_movie.html', users_id=user_id, movies=list_of_movies_data)

    else:
        return render_template('delete_movie.html', user_id=user_id, movie_id=movie_id)


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error():
    return render_template("500.html"), 500


@app.errorhandler(400)
def data_error():
    return render_template("400.html", error_message="Not valid data"), 400


if __name__ == '__main__':
    app.run(debug=True)
