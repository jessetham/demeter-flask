from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Flask SQLAlchemy
db = SQLAlchemy()
# Flask Migrate
migrate = Migrate()

def create_app(config_class=Config):
    # Flask application
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Bind extensions to app instance
    db.init_app(app)
    migrate.init_app(app, db)

    # Import API blueprints and bind to app
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

from app import models
