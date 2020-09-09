#!/usr/bin/python3
""" This file contain code that allow check the status of the AirBnB_clone API
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
h = getenv('HBNB_API_HOST', '0.0.0.0')
p = getenv('HBNB_API_PORT', '5000')


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host=h, port=p, threaded=True)
