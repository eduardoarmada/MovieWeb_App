import json
from .DataManagerInterface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_data(self):
        """Retrieves all the data stored in the json file"""
        with open(self.filename, 'r') as file:
            return json.loads(file.read())

    def get_all_users(self):
        """Returns the names of all the users available in the json file"""
        # Return a list of all users
        with open(self.filename, 'r') as file:
            data = json.loads(file.read())

        return [user.get('name') for user in data.values()]

    def get_user_movies(self, user_id):
        """Returns the name of all the movies of the user passed as argument"""
        # Return a list of all movies for a given user
        with open(self.filename, 'r') as file:
            data = json.loads(file.read())

        return data[user_id].get('movies')

    def add_user(self, name):
        """Adds a user to the json file/persistent storage"""
        with open(self.filename, 'r') as file:
            data = json.loads(file.read())

        users_id = max([int(user_id) for user_id in data.keys()]) + 1
        data[str(users_id)] = {'name': name, 'movies': []}

        with open(self.filename, 'w') as file:
            file.write(json.dumps(data))

    def update_user_movie(self, user_id, movie_id, movie_data):
        """Updates the specified movie of the specified user with the specified data"""
        user_movies = self.get_user_movies(user_id)
        for movie in user_movies:
            if movie['id'] == movie_id:
                for data in movie_data.items():
                    movie[data[0]] = data[1]
            break

        with open(self.filename, 'r') as file:
            data = json.loads(file.read())

        data[user_id]['movies'] = user_movies

        with open(self.filename, 'w') as file:
            file.write(json.dumps(data))

    def add_user_movie(self, user_id, movie_data):
        """Adds a movie to the selected user using the passed by argument data"""
        with open(self.filename, 'r') as file:
            data = json.loads(file.read())

        if not self.get_user_movies(user_id):
            new_movies_id = 1

        else:
            new_movies_id = max([int(movie['id']) for movie in self.get_user_movies(user_id)]) + 1
        new_movie = {'id': new_movies_id, 'name': movie_data[0], 'director': movie_data[-1],
                     'year': movie_data[1], 'rating': movie_data[2], 'poster': movie_data[3]}

        data[user_id]['movies'].append(new_movie)

        with open(self.filename, 'w') as file:
            file.write(json.dumps(data))

    def delete_user_movie(self, user_id, movie_id):
        """Deletes the movie that matches the id in the user selected from the json file/persistent storage"""
        user_movies = self.get_user_movies(user_id)
        movies_to_keep = []

        for movie in user_movies:
            if movie['id'] == movie_id:
                continue
            movies_to_keep.append(movie)

        with open(self.filename, 'r') as file:
            data = json.loads(file.read())

        data[user_id]['movies'] = movies_to_keep

        with open(self.filename, 'w') as file:
            file.write(json.dumps(data))
