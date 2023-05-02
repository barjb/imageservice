from flask import Blueprint
from service import health

bp = Blueprint('service', __name__)
bp.route('/health', methods=['GET'])(health)
