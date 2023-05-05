from flask import Blueprint
from service import health, get_image, get_images, event
from service import delete_image

bp = Blueprint("service", __name__)
bp.route("/health", methods=["GET"])(health)
bp.route("/images", methods=["GET"])(get_images)
bp.route("/images/<string:uuid>", methods=["GET"])(get_image)
bp.route("/images/<string:uuid>", methods=["DELETE"])(delete_image)
bp.route("/event", methods=["GET"])(event)
