from flask import Blueprint
from flask import current_app
import logging

admin_api_bp = Blueprint("admin_api", __name__)

logger = logging.getLogger(__name__)

@admin_api_bp.route("/")
def main():
    current_app.logger.debug("Admin request")
    return "Hello admin!"