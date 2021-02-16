from flask import Flask, render_template, redirect, jsonify, request
from flask_pymongo import PyMongo
import pymongo
import sys

app = Flask(__name__)
# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.movies_db
movies = db.movie_table

###############################################################################################
# Base route on bring up
@app.route("/")
def index():
    return render_template("home.html")

###############################################################################################
# maps route
@app.route("/maps")
def maps():
    return render_template("maps.html")

###############################################################################################
# scatter route
@app.route("/scatter")
def scatter():
    return render_template("scatter.html")

###############################################################################################
# word cloud route
@app.route("/wordcloud", methods=['POST', 'GET'])
def wordcloud():
    genre = "Action"
    text_string = "All work and no play makes jack a dull boy."
    if request.method == "POST":
        genre = request.form['selGenre']
        print("--------------------> Selected: " + genre)
        query = {
                "genres":
                    {
                        "$regex": f'.*{genre}.*',
                        "$options": "i" # case-insensitive
                    }
                }
        genre_match = movies.find(query)
        print("---------------------> Count Match: " + str(genre_match.count(True)))
        text_string = ""
        for cursor in genre_match:
            text_string += cursor.get("keywords") + ":"

    return render_template("cloud.html", text_string = text_string)

if __name__ == "__main__":
    app.run(debug=True)