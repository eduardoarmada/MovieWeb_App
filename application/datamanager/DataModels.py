from MovieWeb_App.application import app

data_manager = app.data_manager


class User(data_manager.db.Model):
    __tablename__ = "users"

    user_id = data_manager.db.Column(data_manager.db.Integer)
    user_name = data_manager.db.Column(data_manager.db.String)
    user_movies = data_manager.db.Column(data_manager.db.String)


class Movie(data_manager.db.Model):
    __tablename__ = "movies"

    movie_id = data_manager.db.Column(data_manager.db.Integer)
    movie_title = data_manager.db.Column(data_manager.db.String)
    movie_director = data_manager.db.Column(data_manager.db.String)
    movie_year = data_manager.db.Column(data_manager.db.Integer)
    movie_rating = data_manager.db.Column(data_manager.db.Integer)
    movie_poster = data_manager.db.Column(data_manager.db.String)
