from flask_sqlalchemy import SQLAlchemy
from .DataManagerInterface import DataManagerInterface


class SQLiteDataManager(DataManagerInterface):
    def __init__(self):
        self.db = SQLAlchemy()

    def create_app(self, app):
        self.db.init_app(app)
        with app.app_context():
            self.db.metadata.create_all(bind=self.db.engine)
        return app

    def get_all_data(self):
        users_data = User.query.all()
        movies_data = Movie.query.all()

        shaped_data = {user.user_id: {"name": user.user_name, "movies": [{'id': movie.movie_id, 'name': movie.movie_title, 'director': movie.movie_director, 'year': movie.movie_year, 'rating': movie.movie_rating, 'poster': movie.movie_poster} for movie in movies_data if str(movie.movie_id) in user.user_movies.split(",")]} for user in users_data}
        print(shaped_data)
        return shaped_data

    def get_all_users(self):
        return [user.get['name'] for user in self.get_all_data()]

    def get_user_movies(self, user_id):
        movies_id = User.query.filter_by(user_id=user_id).first().user_movies.split(",")
        print(movies_id)
        movies_list = [{'id': movie.movie_id, 'name': movie.movie_title, 'director': movie.movie_director, 'year': movie.movie_year, 'rating': movie.movie_rating, 'poster': movie.movie_poster} for movie in Movie.query.all() if str(movie.movie_id) in movies_id]
        return movies_list

    def add_user(self, name):
        user_to_add = User(user_name=name, user_movies="")
        self.db.session.add(user_to_add)
        self.db.session.commit()

    def add_user_movie(self, user_id, movie_data):
        """Adds a movie to the selected user using the passed by argument data"""
        movie_to_add = Movie(movie_title=movie_data[0], movie_director=movie_data[-1], movie_year=movie_data[1], movie_rating=movie_data[2], movie_poster=movie_data[3])
        id_movie = str(Movie.query.order_by(Movie.movie_id).all()[-1].movie_id + 1)
        print(id_movie)
        user = User.query.filter_by(user_id=user_id).first()

        if user.user_movies == "":
            user.user_movies = id_movie
        else:
            user.user_movies = user.user_movies + "," + id_movie

        self.db.session.add(movie_to_add)
        self.db.session.commit()

    def update_user_movie(self, user_id, movie_id, movie_data):
        """Updates the specified movie of the specified user with the specified data"""
        movie_to_update = Movie.query.filter_by(movie_id=movie_id).first()

        if movie_data.get('name'):
            movie_to_update.movie_title = movie_data.get('name')
        if movie_data.get('year'):
            movie_to_update.movie_title = movie_data.get('year')
        if movie_data.get('director'):
            movie_to_update.movie_title = movie_data.get('director')
        if movie_data.get('rating'):
            movie_to_update.movie_title = movie_data.get('rating')

        self.db.session.commit()

    def delete_user_movie(self, user_id, movie_id):
        """Deletes the movie that matches the id in the user selected from the json file/persistent storage"""
        self.db.session.delete(Movie.query.filter_by(movie_id=movie_id).first())
        self.db.session.commit()


data_manager = SQLiteDataManager()


class User(data_manager.db.Model):
    __tablename__ = "users"

    user_id = data_manager.db.Column(data_manager.db.Integer, primary_key=True)
    user_name = data_manager.db.Column(data_manager.db.String)
    user_movies = data_manager.db.Column(data_manager.db.String)


class Movie(data_manager.db.Model):
    __tablename__ = "movies"

    movie_id = data_manager.db.Column(data_manager.db.Integer, primary_key=True)
    movie_title = data_manager.db.Column(data_manager.db.String)
    movie_director = data_manager.db.Column(data_manager.db.String)
    movie_year = data_manager.db.Column(data_manager.db.Integer)
    movie_rating = data_manager.db.Column(data_manager.db.Integer)
    movie_poster = data_manager.db.Column(data_manager.db.String)
