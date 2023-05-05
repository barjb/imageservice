from flask import Flask
import os
from extensions import db

from config import Config


def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 8 * 1000 * 1000
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.POSTGRES_URL

    from images.api import bp as images_bp

    app.register_blueprint(images_bp)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(threaded=True, host="0.0.0.0", port=5000, debug=True)
