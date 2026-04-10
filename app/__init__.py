"""Application package initialization for the Flask backend."""

from flask import Flask
from flasgger import Swagger

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'System Monitor API',
    'uiversion': 3,
}
Swagger(app)

from app import routes  # noqa: E402, F401
