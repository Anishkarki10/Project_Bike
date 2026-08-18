from flask import Blueprint

from app.controllers.admin_controller import AdminController
from app.auth import admin_required
from app.extensions import limiter


class AdminRoutes:

    # =========================================================
    # INITIALIZE ADMIN BLUEPRINT
    # =========================================================
    def __init__(self):

        self.bp = Blueprint(
            "admin",
            __name__,
            url_prefix="/admin"
        )

        self.controller = AdminController()

    # =========================================================
    # REGISTER ROUTES
    # =========================================================
    def register(self):

        # =====================================================
        # LOGIN
        #
        # Rate limited to reduce brute-force attempts.
        # =====================================================
        login_handler = limiter.limit(
            "5 per minute; 20 per hour"
        )(
            self.controller.login
        )

        self.bp.route(
            "/login",
            methods=[
                "GET",
                "POST"
            ]
        )(
            login_handler
        )


        # =====================================================
        # LOGOUT
        #
        # POST only because logout changes session state.
        # CSRF token must be included in logout form.
        # =====================================================
        self.bp.route(
            "/logout",
            methods=[
                "POST"
            ]
        )(
            admin_required(
                self.controller.logout
            )
        )


        # =====================================================
        # DASHBOARD ROOT
        # =====================================================
        self.bp.add_url_rule(
            "/",
            endpoint="root",
            view_func=admin_required(
                self.controller.dashboard
            ),
            methods=[
                "GET"
            ]
        )


        # =====================================================
        # DASHBOARD
        # =====================================================
        self.bp.add_url_rule(
            "/dashboard",
            endpoint="dashboard",
            view_func=admin_required(
                self.controller.dashboard
            ),
            methods=[
                "GET"
            ]
        )


        # =====================================================
        # ALL BIKES
        # =====================================================
        self.bp.route(
            "/bikes",
            methods=[
                "GET"
            ]
        )(
            admin_required(
                self.controller.bikes
            )
        )


        # =====================================================
        # ADD BIKE
        # =====================================================
        self.bp.route(
            "/bikes/add",
            methods=[
                "GET",
                "POST"
            ]
        )(
            admin_required(
                self.controller.add_bike
            )
        )


        # =====================================================
        # EDIT BIKE
        # =====================================================
        self.bp.route(
            "/bikes/<int:bike_id>/edit",
            methods=[
                "GET",
                "POST"
            ]
        )(
            admin_required(
                self.controller.edit_bike
            )
        )


        # =====================================================
        # DELETE BIKE
        # =====================================================
        self.bp.route(
            "/bikes/<int:bike_id>/delete",
            methods=[
                "POST"
            ]
        )(
            admin_required(
                self.controller.delete_bike
            )
        )


        # =====================================================
        # TOGGLE BIKE STATUS
        # =====================================================
        self.bp.route(
            "/bikes/<int:bike_id>/toggle",
            methods=[
                "POST"
            ]
        )(
            admin_required(
                self.controller.toggle_bike_status
            )
        )


        # =====================================================
        # MARK BIKE AS SOLD
        # =====================================================
        self.bp.route(
            "/bikes/<int:bike_id>/sold",
            methods=[
                "GET",
                "POST"
            ],
            endpoint="mark_bike_sold"
        )(
            admin_required(
                self.controller.mark_bike_sold
            )
        )


        # =====================================================
        # CUSTOMER INQUIRIES
        # =====================================================
        self.bp.route(
            "/inquiries",
            methods=[
                "GET"
            ]
        )(
            admin_required(
                self.controller.inquiries
            )
        )


        # =====================================================
        # UPDATE INQUIRY STATUS
        # =====================================================
        self.bp.route(
            "/inquiries/<int:inquiry_id>/status",
            methods=[
                "POST"
            ]
        )(
            admin_required(
                self.controller.update_inquiry
            )
        )


        # =====================================================
        # SETTINGS
        # =====================================================
        self.bp.route(
            "/settings",
            methods=[
                "GET",
                "POST"
            ]
        )(
            admin_required(
                self.controller.settings
            )
        )


        # =====================================================
        # CHANGE ADMIN PASSWORD
        #
        # POST only because it changes account state.
        # CSRF token must be included in the settings form.
        # =====================================================
        self.bp.route(
            "/settings/password",
            methods=[
                "POST"
            ]
        )(
            admin_required(
                self.controller.change_password
            )
        )


        # =====================================================
        # SALES & PROFIT
        # =====================================================
        self.bp.route(
            "/sales",
            methods=[
                "GET"
            ],
            endpoint="sales"
        )(
            admin_required(
                self.controller.sales
            )
        )


        # =====================================================
        # EXPORT SALES CSV
        #
        # GET is acceptable here because exporting does not
        # modify server-side data.
        # =====================================================
        self.bp.route(
            "/sales/export",
            methods=[
                "GET"
            ],
            endpoint="export_sales_csv"
        )(
            admin_required(
                self.controller.export_sales_csv
            )
        )


        # =====================================================
        # RETURN BLUEPRINT
        # =====================================================
        return self.bp