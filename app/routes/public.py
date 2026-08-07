from flask import Blueprint
from app.controllers.public_controller import PublicController


class PublicRoutes:
    def __init__(self):
        self.bp = Blueprint('public', __name__)
        self.controller = PublicController()

    def register(self):
        self.bp.route('/')(self.controller.home)
        self.bp.route('/bikes')(self.controller.bikes)
        self.bp.route('/bikes/<int:bike_id>')(self.controller.bike_detail)
        self.bp.route('/about')(self.controller.about)
        self.bp.route('/contact')(self.controller.contact)
        self.bp.route('/inquiry', methods=['POST'])(self.controller.submit_inquiry)
        return self.bp
