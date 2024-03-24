#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask, render_template
from models.amenity import Amenity
from models.place import Place
from models.state import State
from models import storage


app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def states(state_id=None):
    """display a HTML page with the list of all
    State objects present in DBStorage sorted by name (A->Z)"""
    if state_id is not None:
        state_id = "State." + state_id
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    return render_template(
        "100-hbnb.html", states=states, amenities=amenities, places=places)


@app.teardown_appcontext
def teardown_db(self):
    """closes the storage"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
