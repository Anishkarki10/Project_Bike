from flask import Blueprint

from app.controllers.admin_controller import AdminController
from app.auth import admin_required


class AdminRoutes:

    def __init__(self):

        self.bp = Blueprint(
            "admin",
            __name__,
            url_prefix="/admin"
        )

        self.controller = AdminController()


    def register(self):

        # ==============================
        # AUTH
        # ==============================

        self.bp.route(
            "/login",
            methods=["GET", "POST"]
        )(
            self.controller.login
        )

        self.bp.route(
            "/logout"
        )(
            self.controller.logout
        )


        # ==============================
        # DASHBOARD
        # ==============================

        self.bp.add_url_rule(
            "/",
            endpoint="root",
            view_func=admin_required(
                self.controller.dashboard
            )
        )

        self.bp.add_url_rule(
            "/dashboard",
            endpoint="dashboard",
            view_func=admin_required(
                self.controller.dashboard
            )
        )


        # ==============================
        # BIKES
        # ==============================

        self.bp.route(
            "/bikes",
            methods=["GET"]
        )(
            admin_required(
                self.controller.bikes
            )
        )

        self.bp.route(
            "/bikes/add",
            methods=["GET", "POST"]
        )(
            admin_required(
                self.controller.add_bike
            )
        )

        self.bp.route(
            "/bikes/<int:bike_id>/edit",
            methods=["GET", "POST"]
        )(
            admin_required(
                self.controller.edit_bike
            )
        )

        self.bp.route(
            "/bikes/<int:bike_id>/delete",
            methods=["POST"]
        )(
            admin_required(
                self.controller.delete_bike
            )
        )


        # ==============================
        # TOGGLE BIKE
        # ==============================

        self.bp.route(
            "/bikes/<int:bike_id>/toggle",
            methods=["POST"]
        )(
            admin_required(
                self.controller.toggle_bike_status
            )
        )


        # ==============================
        # MARK BIKE AS SOLD
        # ==============================

        self.bp.route(
            "/bikes/<int:bike_id>/sold",
            methods=["GET", "POST"],
            endpoint="mark_bike_sold"
        )(
            admin_required(
                self.controller.mark_bike_sold
            )
        )


        # ==============================
        # INQUIRIES
        # ==============================

        self.bp.route(
            "/inquiries",
            methods=["GET"]
        )(
            admin_required(
                self.controller.inquiries
            )
        )

        self.bp.route(
            "/inquiries/<int:inquiry_id>/status",
            methods=["POST"]
        )(
            admin_required(
                self.controller.update_inquiry
            )
        )


        # ==============================
        # SETTINGS
        # ==============================

        self.bp.route(
            "/settings",
            methods=["GET", "POST"]
        )(
            admin_required(
                self.controller.settings
            )
        )


        # ==============================
        # SALES
        # ==============================

        self.bp.route(
            "/sales",
            methods=["GET"],
            endpoint="sales"
        )(
            admin_required(
                self.controller.sales
            )
        )


        # ==============================
        # EXPORT SALES CSV
        # ==============================

        self.bp.route(
            "/sales/export",
            methods=["GET"],
            endpoint="export_sales_csv"
        )(
            admin_required(
                self.controller.export_sales_csv
            )
        )


        return self.bp