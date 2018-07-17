from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Flask application
app = Flask(__name__)
app.config.from_object(Config)
# Flask RESTful
api = Api(app, prefix='/api')
# Flask SQLAlchemy
db = SQLAlchemy(app)
# Flask Migrate
migrate = Migrate(app, db)

from app import routes, models