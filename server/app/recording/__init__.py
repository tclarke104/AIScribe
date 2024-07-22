from flask import Blueprint

bp = Blueprint('recordings', __name__)

from app.recording import routes