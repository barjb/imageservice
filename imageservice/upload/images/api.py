from flask import Blueprint
from images.service import post_image, health, event, get_image, get_images
from images.service import delete_image, fix


bp = Blueprint("service", __name__)

bp.route("/images", methods=["POST"])(post_image)
bp.route("/images", methods=["GET"])(get_images)

bp.route("/images/<string:uuid>", methods=["GET"])(get_image)
bp.route("/images/<string:uuid>", methods=["DELETE"])(delete_image)

bp.route("/health", methods=["GET"])(health)
bp.route("/event", methods=["GET"])(event)
bp.route("/fix", methods=["GET"])(fix)
