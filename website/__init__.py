# Import necessary modules and functions for Flask, SQLAlchemy, and Flask-Login
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initialize an instance of SQLAlchemy for interacting with the database and define the name to user.db
db = SQLAlchemy()
DB_NAME = "user.db"

# Function to create and configure the Flask application
def create_app():
    # Initialize app
    app = Flask(__name__)

    # For security purposes, session management, SQLite
    app.config['SECRET_KEY'] = 'CcNpmOazljhYhMwhAtSHuyxY9iBF818ytUMWI8ZmWzJ3pawhr1'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Import views and auth blueprints for app
    from .views import views
    from .auth import auth

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models which are the structure of the databases
    from .models import User, Deposit, GameStats

    # Calls function defined below to create databases
    create_database(app)

    # Initialize the LoginManager, which handles user session and authentication
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Retrieves user by their ID from the database
    @login_manager.user_loader
    def load_user(id):
        # Returns the User object associated with the given ID
        return User.query.get(int(id))

    return app

# Function that actually creates databases
def create_database(app):
    with app.app_context():
        if not path.exists('website/' + DB_NAME):
            db.create_all()