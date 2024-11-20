import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, user_logged_in, user_login_attempt
from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)

# Enable debug mode
app.debug = True

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,  # Change to DEBUG level
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app.logger.setLevel(logging.DEBUG)

Session(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

# Log successful sign-ins
@user_logged_in.connect_via(app)
def log_successful_login(sender, user):
    app.logger.info(f"User {user.id} logged in successfully.")

# Log failed sign-ins
@user_login_attempt.connect_via(app)
def log_failed_login(sender, user, **extra):
    app.logger.warning(f"Failed login attempt for user {user.id if user else 'unknown'}.")

import FlaskWebProject.views
