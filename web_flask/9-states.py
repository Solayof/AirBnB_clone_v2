#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask, render_template
from models.state import State
from models import storage


app = Flask(__name__)


@app.route("/states", strict_slashes=False)
@app.route("/states/<state_id>", strict_slashes=False)
def states(state_id=None):
    """display a HTML page with the list of all
    State objects present in DBStorage sorted by name (A->Z)"""
    if state_id is not None:
        state_id = "State." + state_id
    states = storage.all(State)
    print(state_id in states)
    return render_template(
        "9-states.html", states=states, state_id=state_id)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
