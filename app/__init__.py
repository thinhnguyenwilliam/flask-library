from flask import Flask
from .config import Config
from .extensions import db, ma, jwt
from .routes import register_blueprints
from urllib.parse import urlparse

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Print full DB URI (optional)
    print("Full DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])

    # Parse the DB name from the URI
    parsed = urlparse(app.config["SQLALCHEMY_DATABASE_URI"])
    db_name = parsed.path.lstrip("/")  # removes leading slash
    print("Database name:", db_name)

    '''
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    
    '''
    register_blueprints(app)

    return app
