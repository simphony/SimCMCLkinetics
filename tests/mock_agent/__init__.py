"""This module defines flask app factory method"""

from flask import Flask
from mock_agent.routes.public import kinetics_agent_bp
from mock_agent.routes.admin import admin_api_bp
import os
import logging
import logging.config

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler(os.path.join(THIS_DIR,"mock_agent.log"),'w'),
                              logging.StreamHandler()])
logging.getLogger("werkzeug").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


def create_app(config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    if config is not None:
        # load the test config if passed in
        app.config.from_mapping(config)
    else:
        app.config.from_pyfile("config.py", silent=False)

    # Register Blueprints
    app.register_blueprint(kinetics_agent_bp, url_prefix="/")
    app.register_blueprint(admin_api_bp, url_prefix="/admin")

    return app
