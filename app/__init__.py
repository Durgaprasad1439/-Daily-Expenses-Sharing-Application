from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import initialize_routes
    initialize_routes(app)

    return app