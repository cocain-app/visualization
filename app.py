import os
import sys
import json
import psycopg2
from flask import Flask, render_template, request, jsonify

# Configure flask
app = Flask(__name__)

# Check for secrets
if(not('DATABASE_HOST' in os.environ and
       'DATABASE_PORT' in os.environ and
       'DATABASE_USER' in os.environ and
       'DATABASE_PASSWORD' in os.environ and
       'DATABASE_DATABASE' in os.environ)):
    print("Environment variables missing.")
    sys.exit()


# Connect to database
try:
    conn = psycopg2.connect(
        "dbname='%s' user='%s' host='%s' password='%s'" %
        (
            os.environ["DATABASE_DATABASE"],
            os.environ["DATABASE_USER"],
            os.environ["DATABASE_HOST"],
            os.environ["DATABASE_PASSWORD"],
        )
    )
    cursor = conn.cursor()
    print("Connected to database")

except Exception:
    print("Database connection not possibe.")
    sys.exit()

# Flask Routes
@app.route("/")
def index():

    # Number of Songs
    SQL = "SELECT Count(id) FROM Songs"
    cursor.execute(SQL)
    number_of_songs = cursor.fetchone()[0]

    # Number of Transitions
    SQL = "SELECT Count(song_from) FROM Transitions"
    cursor.execute(SQL)
    number_of_transitions = cursor.fetchone()[0]

    # Number of Artists
    SQL = "SELECT Count(id) FROM Artists"
    cursor.execute(SQL)
    number_of_artists = cursor.fetchone()[0]

    # Number of Djs
    SQL = "SELECT Count(id) FROM Djs"
    cursor.execute(SQL)
    number_of_djs = cursor.fetchone()[0]

    # Number of Sets
    SQL = "SELECT Count(id) FROM Sets"
    cursor.execute(SQL)
    number_of_sets = cursor.fetchone()[0]

    return render_template('index.html', number_of_songs=number_of_songs, number_of_transitions=number_of_transitions, number_of_artists=number_of_artists, number_of_djs=number_of_djs, number_of_sets=number_of_sets)


@app.route("/sigma")
def sigma():
    data = {
        "nodes": [],
        "links": []
    }

    SQL = "SELECT songs.id, songs.title, COUNT(transitions.song_from) FROM songs LEFT OUTER JOIN transitions ON songs.id = transitions.song_from GROUP BY songs.id"
    cursor.execute(SQL)
    for song in cursor.fetchall():
        data["nodes"].append({
            "id": song[0],
            "label": song[1],
            "weight": song[2],
        })

    SQL = "SELECT song_from, song_to FROM Transitions"
    cursor.execute(SQL)
    for index, transition in enumerate(cursor.fetchall()):
        data["links"].append({
            "source": transition[0],
            "target": transition[1]
        })

    return jsonify(data)
