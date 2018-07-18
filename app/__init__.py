from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Flask application
app = Flask(__name__)
app.config.from_object(Config)
# Flask SQLAlchemy
db = SQLAlchemy(app)
# Flask Migrate
migrate = Migrate(app, db)

from app import api, models