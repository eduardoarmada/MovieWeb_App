from flask import Flask
from datamanager.json_data_manager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('movies.json')  # Use the appropriate path to your JSON file


@app.route("/")
def home():
    return "hello world"


if __name__ == '__main__':
    app.run(debug=True)
