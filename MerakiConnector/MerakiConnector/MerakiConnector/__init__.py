"""
The flask application package.
"""

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "this is the secret key"

import MerakiConnector.views
