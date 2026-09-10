from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config


# Initialize extensions (but don't bind them to an app yet)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # ✅ Load configuration
    app.config.from_object(Config)

    # ✅ Apply CORS globally
    CORS(app, supports_credentials=True)

    # ✅ Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # ✅ Import models (to register them with SQLAlchemy)
    from app import models  # Ensure this is after `db.init_app(app)`

    # ✅ Import and register blueprints
    from app.graphql_routes import graphql_bp

    app.register_blueprint(graphql_bp, url_prefix="/graphql/")

    # ✅ Health check endpoint
    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app
