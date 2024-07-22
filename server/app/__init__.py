from flask import Flask

from config import Config
from app.extensions import db
from flask_cors import CORS


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    # Initialize Flask extensions here
    db.init_app(app)

    CORS(app)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.recording import bp as recordings_bp
    app.register_blueprint(recordings_bp, url_prefix='/recordings')


    return app