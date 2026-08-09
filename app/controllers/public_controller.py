import re

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.models.bike import Bike
from app.models.inquiry import Inquiry
from app.models.settings import Settings


class PublicController:

    # =========================================================
    # INITIALIZE MODELS
    # =========================================================
    def __init__(self):

        self.bike_model = Bike()
        self.inquiry_model = Inquiry()
        self.settings_model = Settings()

    # =========================================================
    # COMMON TEMPLATE DATA
    # =========================================================
    def _common(self):

        return {
            "settings": self.settings_model.get()
        }

    # =========================================================
    # CLEAN TEXT
    # =========================================================
    def _clean_text(
        self,
        value,
        max_length,
        required=False
    ):

        value = (
            value
            or ""
        ).strip()

        if required and not value:
            return None

        if len(value) > max_length:
            return None

        # Reject control characters except:
        # tab, newline and carriage return.
        for char in value:

            if (
                ord(char) < 32
                and char not in {
                    "\t",
                    "\n",
                    "\r"
                }
            ):
                return None

        return value

    # =========================================================
    # VALIDATE PHONE
    # =========================================================
    def _valid_phone(
        self,
        value
    ):

        value = (
            value
            or ""
        ).strip()

        if not value:
            return None

        if len(value) > 40:
            return None

        # Allows examples such as:
        #
        # 9860541990
        # +9779860541990
        # +977 9860541990
        # 01-1234567
        #
        if not re.fullmatch(
            r"[0-9+\-\s()]{7,40}",
            value
        ):
            return None

        digits = re.sub(
            r"\D",
            "",
            value
        )

        if not (
            7
            <= len(digits)
            <= 15
        ):
            return None

        return value

    # =========================================================
    # VALIDATE EMAIL
    # =========================================================
    def _valid_email(
        self,
        value
    ):

        value = (
            value
            or ""
        ).strip().lower()

        # Optional field
        if not value:
            return None

        if len(value) > 150:
            return None

        if not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            value
        ):
            return None

        return value

    # =========================================================
    # VALIDATE PRICE FILTER
    # =========================================================
    def _price_filter(
        self,
        value
    ):

        value = (
            value
            or ""
        ).strip()

        if not value:
            return None

        try:

            number = float(
                value
            )

        except (
            TypeError,
            ValueError
        ):
            return None

        if (
            number < 0
            or number > 100_000_000
        ):
            return None

        return number

    # =========================================================
    # HOME
    # =========================================================
    def home(self):

        data = self._common()

        data["bikes"] = (
            self.bike_model
            .get_available_featured(
                6
            )
        )

        return render_template(
            "public/home.html",
            **data
        )

    # =========================================================
    # AVAILABLE BIKES
    # =========================================================
    def bikes(self):

        # -----------------------------------------------------
        # Public visitors can only browse available inventory.
        # -----------------------------------------------------
        status = "available"

        search = self._clean_text(
            request.args.get(
                "search",
                ""
            ),
            max_length=100
        )

        brand = self._clean_text(
            request.args.get(
                "brand",
                ""
            ),
            max_length=100
        )

        category = (
            request.args.get(
                "category",
                ""
            )
            .strip()
            .lower()
        )

        if category not in {
            "",
            "motorcycle",
            "scooter"
        }:
            category = ""

        min_price = self._price_filter(
            request.args.get(
                "min_price"
            )
        )

        max_price = self._price_filter(
            request.args.get(
                "max_price"
            )
        )

        if (
            min_price is not None
            and max_price is not None
            and min_price > max_price
        ):

            min_price = None
            max_price = None

        filters = {
            "search":
                search or None,

            "brand":
                brand or None,

            "category":
                category or None,

            "status":
                status,

            "min_price":
                min_price,

            "max_price":
                max_price
        }

        rows = (
            self.bike_model
            .get_all(
                **filters
            )
        )

        for bike in rows:

            bike["images"] = (
                self.bike_model
                .get_images(
                    bike["id"]
                )
            )

        data = self._common()

        data.update({
            "bikes":
                rows,

            "brands":
                self.bike_model
                .get_brands(),

            "filters":
                filters
        })

        return render_template(
            "public/bikes.html",
            **data
        )

    # =========================================================
    # BIKE DETAILS
    # =========================================================
    def bike_detail(
        self,
        bike_id
    ):

        bike = (
            self.bike_model
            .find_by_id(
                bike_id
            )
        )

        if not bike:

            return render_template(
                "notfound.html"
            ), 404

        # -----------------------------------------------------
        # Never expose draft inventory publicly.
        #
        # Sold bikes remain viewable here.
        # If you do NOT want sold bikes visible,
        # change this to:
        #
        # if bike.get("status") != "available":
        # -----------------------------------------------------
        if bike.get(
            "status"
        ) == "draft":

            return render_template(
                "notfound.html"
            ), 404

        bike["images"] = (
            self.bike_model
            .get_images(
                bike_id
            )
        )

        cover_image = bike.get(
            "cover_image"
        )

        if (
            cover_image
            and cover_image
            not in bike["images"]
        ):

            bike["images"].insert(
                0,
                cover_image
            )

        if not bike["images"]:

            bike["images"] = (
                [cover_image]
                if cover_image
                else []
            )

        bike["feature_list"] = [

            feature.strip()

            for feature in (
                bike.get(
                    "features"
                )
                or ""
            ).split(",")

            if feature.strip()

        ]

        data = self._common()

        data["bike"] = bike

        return render_template(
            "public/bike_detail.html",
            **data
        )

    # =========================================================
    # ABOUT
    # =========================================================
    def about(self):

        return render_template(
            "public/about.html",
            **self._common()
        )

    # =========================================================
    # CONTACT
    # =========================================================
    def contact(self):

        data = self._common()

        data["bikes"] = (
            self.bike_model
            .get_all(
                status="available"
            )
        )

        return render_template(
            "public/contact.html",
            **data
        )

    # =========================================================
    # SUBMIT INQUIRY
    # =========================================================
    def submit_inquiry(self):

        # -----------------------------------------------------
        # NAME
        # -----------------------------------------------------
        name = self._clean_text(
            request.form.get(
                "name"
            ),
            max_length=120,
            required=True
        )

        if not name:

            flash(
                "Please enter a valid name.",
                "danger"
            )

            return redirect(
                request.referrer
                or url_for(
                    "public.contact"
                )
            )

        # -----------------------------------------------------
        # PHONE
        # -----------------------------------------------------
        phone = self._valid_phone(
            request.form.get(
                "phone"
            )
        )

        if not phone:

            flash(
                "Please enter a valid phone number.",
                "danger"
            )

            return redirect(
                request.referrer
                or url_for(
                    "public.contact"
                )
            )

        # -----------------------------------------------------
        # EMAIL
        # -----------------------------------------------------
        email_raw = (
            request.form.get(
                "email",
                ""
            )
            .strip()
        )

        email = (
            self._valid_email(
                email_raw
            )
        )

        if (
            email_raw
            and email is None
        ):

            flash(
                "Please enter a valid email address.",
                "danger"
            )

            return redirect(
                request.referrer
                or url_for(
                    "public.contact"
                )
            )

        # -----------------------------------------------------
        # MESSAGE
        # -----------------------------------------------------
        message = self._clean_text(
            request.form.get(
                "message"
            ),
            max_length=2000,
            required=True
        )

        if not message:

            flash(
                "Please enter a valid message.",
                "danger"
            )

            return redirect(
                request.referrer
                or url_for(
                    "public.contact"
                )
            )

        # Require at least some meaningful non-whitespace text.
        meaningful_message = re.sub(
            r"\s+",
            "",
            message
        )

        if len(meaningful_message) < 3:

            flash(
                "Please enter a more detailed message.",
                "danger"
            )

            return redirect(
                request.referrer
                or url_for(
                    "public.contact"
                )
            )

        # -----------------------------------------------------
        # BIKE
        #
        # Never trust a bike name supplied by the browser.
        # -----------------------------------------------------
        bike_id_raw = (
            request.form.get(
                "bike_id",
                ""
            )
            .strip()
        )

        bike_id = None
        bike_name = None

        if bike_id_raw:

            try:

                bike_id = int(
                    bike_id_raw
                )

            except (
                TypeError,
                ValueError
            ):

                flash(
                    "Invalid bike selection.",
                    "danger"
                )

                return redirect(
                    url_for(
                        "public.contact"
                    )
                )

            if bike_id <= 0:

                flash(
                    "Invalid bike selection.",
                    "danger"
                )

                return redirect(
                    url_for(
                        "public.contact"
                    )
                )

            bike = (
                self.bike_model
                .find_by_id(
                    bike_id
                )
            )

            if not bike:

                flash(
                    "The selected bike does not exist.",
                    "danger"
                )

                return redirect(
                    url_for(
                        "public.contact"
                    )
                )

            if (
                bike.get(
                    "status"
                )
                != "available"
            ):

                flash(
                    "This bike is no longer available.",
                    "danger"
                )

                return redirect(
                    url_for(
                        "public.bikes"
                    )
                )

            # ---------------------------------------------
            # Trusted server-side value.
            # ---------------------------------------------
            bike_name = bike.get(
                "name"
            )

        # -----------------------------------------------------
        # STORE INQUIRY
        # -----------------------------------------------------
        self.inquiry_model.create({
            "name":
                name,

            "phone":
                phone,

            "email":
                email,

            "bike_id":
                bike_id,

            "bike_interested":
                bike_name,

            "message":
                message
        })

        flash(
            "Thanks! Your inquiry has been sent to Supa Auto Link.",
            "success"
        )

        # -----------------------------------------------------
        # REDIRECT
        # -----------------------------------------------------
        if bike_id:

            return redirect(
                url_for(
                    "public.bike_detail",
                    bike_id=bike_id
                )
            )

        return redirect(
            url_for(
                "public.contact"
            )
        )