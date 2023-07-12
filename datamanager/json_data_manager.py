import json
import os
from .DataManagerInterface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_data(self):
        with open(self.filename, 'r') as file:
            return json.loads(file.read())

    def get_all_users(self):
        # Return a list of all users
        with open(self.filename, 'r') as file:
            data = json.loads(file.read())

        return [user.get('name') for user in data.values()]

    def get_user_movies(self, user_id):
        # Return a list of all movies for a given user
        with open(self.filename, 'r') as file:
            data = json.loads(file.read())

        return data[user_id].get('movies')

    def add_user(self, name):
        with open(self.filename, 'r') as file:
            data = json.loads(file.read())

        users_id = max([int(user_id) for user_id in data.keys()]) + 1
        data[str(users_id)] = {'name': name, 'movies': []}

        with open(self.filename, 'w') as file:
            file.write(json.dumps(data))

    def update_user_movie(self, user_id, movie_id, movie_data):
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
        with open(self.filename, 'r') as file:
            data = json.loads(file.read())

        new_movies_id = max([int(movie['id']) for movie in self.get_user_movies(user_id)]) + 1
        new_movie = {'id': new_movies_id, 'name': movie_data[0], 'director': movie_data[-1],
                     'year': movie_data[1], 'rating': movie_data[2], 'poster': movie_data[3]}

        data[user_id]['movies'].append(new_movie)

        with open(self.filename, 'w') as file:
            file.write(json.dumps(data))

    def delete_user_movie(self, user_id, movie_id):
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


