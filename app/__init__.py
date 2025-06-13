"""
Flask app factory and extension initialization for Loyalty Reward Engine.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from app.spin import spin_bp
from app.prize import prize_bp

# Load environment variables from .env
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(spin_bp)
    app.register_blueprint(prize_bp)

    return app

__all__ = ["create_app", "db", "migrate", "jwt"] 