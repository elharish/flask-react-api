from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, bcrypt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Enable CORS for all origins
    CORS(app)

    # Register blueprints
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    # Auto-create tables
    with app.app_context():
        db.create_all()
        print("[OK] Database tables are ready.")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)