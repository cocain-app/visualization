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

    SQL = "SELECT songs.id, songs.title, artists.name, count(songs.id) AS weight FROM songs JOIN artists ON songs.artist_id = artists.id INNER JOIN (SELECT song_from, song_to FROM Transitions INNER JOIN (SELECT songs.id as id FROM songs JOIN transitions on transitions.song_from = songs.id GROUP BY songs.id ORDER BY Count(songs.id) DESC LIMIT 500) AS U ON u.id = song_from) as u on u.song_from = songs.id GROUP BY songs.id, artists.name ORDER BY weight DESC LIMIT 500"
    cursor.execute(SQL)
    song_ids = []
    for song in cursor.fetchall():
        song_ids.append(song[0])
        data["nodes"].append({
            "id": song[0],
            "title": song[1],
            "artist": song[2],
            "weight": song[3],
        })

    SQL = "SELECT song_from, song_to, count(song_from) FROM Transitions INNER JOIN (SELECT songs.id as id FROM songs JOIN transitions on transitions.song_from = songs.id GROUP BY songs.id ORDER BY Count(songs.id) DESC LIMIT 500) AS U ON u.id = song_from GROUP BY song_from, song_to"
    cursor.execute(SQL)
    for index, transition in enumerate(cursor.fetchall()):
        if(transition[0] in song_ids and transition[1] in song_ids):
            data["links"].append({
                "source": transition[0],
                "target": transition[1],
                "weight": transition[2]
            })

    return jsonify(data)
