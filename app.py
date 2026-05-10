from flask import Flask
from flask_cors import CORS

from config import Config
from models import db
from routes.simulacion import simulacion_bp
from routes.solicitudes import solicitudes_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, origins="*")
    db.init_app(app)

    app.register_blueprint(simulacion_bp)
    app.register_blueprint(solicitudes_bp)

    @app.route("/")
    def health():
        return {"mensaje": "Roda API v1.0.0"}

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
