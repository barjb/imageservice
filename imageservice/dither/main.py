from flask import Flask


def create_app():
    app = Flask(__name__)

    from api import bp as dither_bp
    app.register_blueprint(dither_bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(threaded=True, host='0.0.0.0', port=5000, debug=True)
