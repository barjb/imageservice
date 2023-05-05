from flask import Flask
import os
from extensions import db

POSTGRES_URL = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}"


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URL

    from api import bp as dither_bp
    app.register_blueprint(dither_bp)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(threaded=True, host='0.0.0.0', port=5000, debug=True)
