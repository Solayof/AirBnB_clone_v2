#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask


app = Flask(__name__)

@app.route('/', strict_slashes=False)
def index():
    """returns Hello HBNB"""
    return "Hello HBNB!"

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """return HBNB"""
    return "HBNB"

@app.route('/c/<text>', strict_slashes=False)
def c_fun(text):
    """Display 'C ' followed by the value of the text variable"""
    return "C " + text.replace("_", " ")

# @app.route('/python', strict_slashes=False)
# @app.route('/python/<text>', strict_slashes=False)
# def python_cool(text="is cool"):
#     """
#     display “Python ”, followed by the value of the text variable
#     The default value of text is “is cool"
#     """
#     return "Python " + text.replace("_", " ")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
