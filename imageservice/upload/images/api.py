from flask import Blueprint
from images.service import upload_file, health, event, get_file

bp = Blueprint('service', __name__)
bp.route('/upload', methods=['POST'])(upload_file)
bp.route('/id/<string:uuid>', methods=['GET'])(get_file)
bp.route('/health', methods=['GET'])(health)
bp.route('/event', methods=['GET'])(event)
