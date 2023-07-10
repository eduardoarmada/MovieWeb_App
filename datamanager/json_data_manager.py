import json
from DataManagerInterface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        # Return a list of all users
        with open(self.filename, 'r') as file:
            data = json.loads(file.read())

        return [user['name'] for user in data.values()]

    def get_user_movies(self, user_id):
        # Return a list of all movies for a given user
        with open(self.filename, 'r') as file:
            data = json.loads(file.read())

        return data[user_id].get('movies')

    def update_user_movie(self, movie_name):
        pass

    def add_user_movie(self, movie_data):
        pass

    def delete_user_movie(self, movie_name):
        pass