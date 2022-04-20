from flask import Blueprint, request

admin_api_bp = Blueprint("admin_api", __name__)


@admin_api_bp.route("/")
def main():
    return "Hello admin!"