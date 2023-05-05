from flask import Flask
from extensions import db

from config import Config


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.POSTGRES_URL

    from api import bp as dither_bp

    app.register_blueprint(dither_bp)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(threaded=True, host="0.0.0.0", port=5000, debug=True)
