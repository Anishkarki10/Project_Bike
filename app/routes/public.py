from flask import Blueprint

from app.controllers.public_controller import PublicController
from app.extensions import limiter


class PublicRoutes:

    def __init__(self):

        self.bp = Blueprint(
            "public",
            __name__
        )

        self.controller = (
            PublicController()
        )

    def register(self):

        # =====================================================
        # HOME
        # =====================================================
        self.bp.route(
            "/"
        )(
            self.controller.home
        )

        # =====================================================
        # AVAILABLE BIKES
        # =====================================================
        self.bp.route(
            "/bikes"
        )(
            self.controller.bikes
        )

        # =====================================================
        # BIKE DETAILS
        # =====================================================
        self.bp.route(
            "/bikes/<int:bike_id>"
        )(
            self.controller.bike_detail
        )

        # =====================================================
        # ABOUT
        # =====================================================
        self.bp.route(
            "/about"
        )(
            self.controller.about
        )

        # =====================================================
        # CONTACT
        # =====================================================
        self.bp.route(
            "/contact"
        )(
            self.controller.contact
        )

        # =====================================================
        # ROBOTS.TXT
        # =====================================================
        self.bp.route(
            "/robots.txt"
        )(
            self.controller.robots_txt
        )

        # =====================================================
        # SITEMAP.XML
        # =====================================================
        self.bp.route(
            "/sitemap.xml"
        )(
            self.controller.sitemap_xml
        )

        # =====================================================
        # SUBMIT INQUIRY
        #
        # Maximum:
        # 5 requests per minute per IP
        # 20 requests per hour per IP
        # =====================================================
        inquiry_handler = (
            limiter.limit(
                "5 per minute; 20 per hour"
            )(
                self.controller
                .submit_inquiry
            )
        )

        self.bp.route(
            "/inquiry",
            methods=[
                "POST"
            ]
        )(
            inquiry_handler
        )

        return self.bp