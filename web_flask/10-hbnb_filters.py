#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask, render_template
from models.state import State
from models import storage


app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def states():
    """display a HTML page with the list of all State objects present in DBStorage sorted by name (A->Z)"""
    amenities = storage.all("Amentity").values()
    states = storage.all("State").values()
    return render_template("10-hbnb_filters.html", states=states, amenities=amenities)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage"""
    storage.close()



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)