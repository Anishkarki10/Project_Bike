from flask import Blueprint
from app.controllers.admin_controller import AdminController
from app.auth import admin_required


class AdminRoutes:
    def __init__(self):
        self.bp = Blueprint('admin', __name__, url_prefix='/admin')
        self.controller = AdminController()

    def register(self):
        self.bp.route('/login', methods=['GET','POST'])(self.controller.login)
        self.bp.route('/logout')(self.controller.logout)
        self.bp.add_url_rule('/', endpoint='root', view_func=admin_required(self.controller.dashboard))
        self.bp.add_url_rule('/dashboard', endpoint='dashboard', view_func=admin_required(self.controller.dashboard))
        self.bp.route('/bikes')(admin_required(self.controller.bikes))
        self.bp.route('/bikes/add', methods=['GET','POST'])(admin_required(self.controller.add_bike))
        self.bp.route('/bikes/<int:bike_id>/edit', methods=['GET','POST'])(admin_required(self.controller.edit_bike))
        self.bp.route('/bikes/<int:bike_id>/delete', methods=['POST'])(admin_required(self.controller.delete_bike))
        self.bp.route('/bikes/<int:bike_id>/toggle', methods=['POST'])(admin_required(self.controller.toggle_bike_status))
        self.bp.route('/inquiries')(admin_required(self.controller.inquiries))
        self.bp.route('/inquiries/<int:inquiry_id>/status', methods=['POST'])(admin_required(self.controller.update_inquiry))
        self.bp.route('/settings', methods=['GET','POST'])(admin_required(self.controller.settings))
        return self.bp
