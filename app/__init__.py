import os

from flask import Flask
from .config import Config
from .extensions import db, ma, jwt, cors
from .routes import register_blueprints
from urllib.parse import urlparse
from log_config import setup_logger, inject_log_metadata
from .middleware import register_middlewares
from .db import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        init_db()

    # Print full DB URI (optional)
    print("Full DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])

    # Parse the DB name from the URI
    parsed = urlparse(app.config["SQLALCHEMY_DATABASE_URI"])
    db_name = parsed.path.lstrip("/")  # removes leading slash
    print("Database name:", db_name)
    db.init_app(app)
    '''
    ma.init_app(app)
    jwt.init_app(app)
    '''

    # Enable CORS
    cors.init_app(app, supports_credentials=True, resources={r"/api/*": {"origins": ["http://localhost:4200",
                                                          "https://your-frontend.com"
                                                          ]}})
    # cors.init_app(app, resources={
    #     r"/api/*": {
    #         "origins": ["http://localhost:4200", "https://myfrontend.com"],
    #         "methods": ["GET", "POST", "PUT", "DELETE"],
    #         "allow_headers": ["Content-Type", "Authorization"]
    #     }
    # })



    # Register middlewares 👇
    register_middlewares(app)

    register_blueprints(app)

    # Set environment (or use ENV variable)
    env = os.environ.get('FLASK_ENV', 'production')
    setup_logger(app, env)
    inject_log_metadata(app)

    return app
