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
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

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
    app.run(debug=True, port=5000)
