from flask import Blueprint

home_bp = Blueprint('base', __name__,
                    template_folder='templates/base')

from . import views
