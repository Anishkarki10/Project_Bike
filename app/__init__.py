import os

from datetime import datetime

from flask import (
    Flask,
    render_template
)

from werkzeug.middleware.proxy_fix import ProxyFix

from app.extensions import (
    csrf,
    limiter
)

from app.models.database import Database
from app.routes.public import PublicRoutes
from app.routes.admin import AdminRoutes

import config


# =========================================================
# CREATE FLASK APPLICATION
# =========================================================
def create_app(testing=False):

    app = Flask(__name__)

    # =====================================================
    # REVERSE PROXY SUPPORT
    #
    # Required when Flask is behind Nginx / Cloudflare.
    # This lets Flask correctly detect:
    #
    # - HTTPS
    # - real hostname
    # - forwarded client IP
    #
    # so url_for(..., _external=True) generates:
    #
    # https://supaautolink.com.np/...
    #
    # instead of:
    #
    # http://127.0.0.1:8000/...
    # =====================================================
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1
    )

    # =====================================================
    # BASIC CONFIGURATION
    # =====================================================
    app.config["SECRET_KEY"] = (
        config.SECRET_KEY
    )

    app.config["TESTING"] = (
        testing
    )


    # =====================================================
    # FILE UPLOAD LIMIT
    # =====================================================
    app.config["MAX_CONTENT_LENGTH"] = (
        config.MAX_CONTENT_LENGTH
    )


    # =====================================================
    # SESSION SECURITY
    # =====================================================
    app.config["SESSION_COOKIE_HTTPONLY"] = (
        True
    )

    app.config["SESSION_COOKIE_SAMESITE"] = (
        "Lax"
    )

    app.config["SESSION_COOKIE_SECURE"] = (
        config.SESSION_COOKIE_SECURE
    )


    # =====================================================
    # UPLOAD FOLDER
    # =====================================================
    app.config["BIKE_UPLOAD_FOLDER"] = os.path.join(
        app.root_path,
        "static",
        "uploads",
        "bikes"
    )

    os.makedirs(
        app.config["BIKE_UPLOAD_FOLDER"],
        exist_ok=True
    )


    # =====================================================
    # INITIALIZE EXTENSIONS
    # =====================================================

    # CSRF protection
    csrf.init_app(
        app
    )

    # Login / route rate limiting
    limiter.init_app(
        app
    )


    # =====================================================
    # DATABASE
    # =====================================================
    if not testing:

        with app.app_context():

            Database.ensure_database()

            Database.create_tables()


    # =====================================================
    # ROUTES
    # =====================================================
    public_routes = (
        PublicRoutes()
    )

    admin_routes = (
        AdminRoutes()
    )

    app.register_blueprint(
        public_routes.register()
    )

    app.register_blueprint(
        admin_routes.register()
    )


    # =====================================================
    # TEMPLATE GLOBALS
    #
    # Makes current_year available to every template.
    # =====================================================
    @app.context_processor
    def inject_globals():

        return {
            "current_year":
                datetime.now().year
        }


    # =====================================================
    # SECURITY HEADERS
    # =====================================================
    @app.after_request
    def add_security_headers(
        response
    ):

        response.headers[
            "X-Content-Type-Options"
        ] = "nosniff"

        response.headers[
            "X-Frame-Options"
        ] = "SAMEORIGIN"

        response.headers[
            "Referrer-Policy"
        ] = (
            "strict-origin-when-cross-origin"
        )

        response.headers[
            "Permissions-Policy"
        ] = (
            "camera=(), "
            "microphone=(), "
            "geolocation=()"
        )

        return response


    # =====================================================
    # 404 ERROR
    # =====================================================
    @app.errorhandler(404)
    def page_not_found(
        error
    ):

        return render_template(
            "notfound.html"
        ), 404


    # =====================================================
    # 413 FILE TOO LARGE
    # =====================================================
    @app.errorhandler(413)
    def file_too_large(
        error
    ):

        return render_template(
            "notfound.html"
        ), 413


    # =====================================================
    # 429 TOO MANY REQUESTS
    # =====================================================
    @app.errorhandler(429)
    def too_many_requests(
        error
    ):

        return (
            "Too many requests. "
            "Please wait and try again.",
            429
        )


    return app