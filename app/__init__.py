from flask import Flask
from .extensions import db, login_manager
from .models.user import User 
from .routes.main import main
from .routes.auth import auth
from .routes.admin import admin
from dotenv import load_dotenv
import datetime

load_dotenv()

def create_app():
    """
    Initializes a Flask web application.
    
    This function sets up and configures the application, including
    database and login manager initialization, as well as registering
    the main, auth, and admin blueprints.
    
    @return A configured Flask web application.
    """
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    @app.context_processor
    def inject_now():
        """
        Injects the current UTC datetime into all templates.
        This makes the 'now' variable globally available in Jinja2.
        """
        return {'now': datetime.datetime.utcnow()}

    @login_manager.user_loader
    def load_user(user_id):
        """
        Loads a user by their user ID.

        @param user_id The ID of the user to load.
        @return The user instance with the given user ID, or None if the user
                does not exist.
        """
        return User.query.get(int(user_id))

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')

    return app
