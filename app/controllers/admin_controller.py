import os
import time
import csv
import io

from datetime import datetime, date

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    current_app,
    Response
)

from werkzeug.utils import secure_filename

from app.models.user import User
from app.models.bike import Bike
from app.models.inquiry import Inquiry
from app.models.settings import Settings

import config


class AdminController:

    # =========================================================
    # INITIALIZE MODELS
    # =========================================================
    def __init__(self):

        self.user_model = User()
        self.bike_model = Bike()
        self.inquiry_model = Inquiry()
        self.settings_model = Settings()

    # =========================================================
    # ADMIN LOGIN
    # =========================================================
    def login(self):

        if session.get("admin_id"):

            return redirect(
                url_for(
                    "admin.dashboard"
                )
            )

        if request.method == "POST":

            email = (
                request.form.get(
                    "email",
                    ""
                )
                .strip()
                .lower()
            )

            password = request.form.get(
                "password",
                ""
            )

            user = (
                self.user_model
                .find_by_email(
                    email
                )
            )

            if (
                not user
                or user.get("role") != "admin"
                or not self.user_model.check_password(
                    user["password"],
                    password
                )
            ):

                flash(
                    "Invalid admin email or password.",
                    "danger"
                )

                return render_template(
                    "admin/login.html"
                )

            session.clear()

            session.permanent = True

            session["admin_id"] = (
                user["id"]
            )

            session["admin_name"] = (
                user["name"]
            )

            session["role"] = (
                user["role"]
            )

            return redirect(
                url_for(
                    "admin.dashboard"
                )
            )

        return render_template(
            "admin/login.html"
        )

    # =========================================================
    # LOGOUT
    # =========================================================
    def logout(self):

        session.clear()

        flash(
            "Logged out successfully.",
            "success"
        )

        return redirect(
            url_for(
                "admin.login"
            )
        )

    # =========================================================
    # DASHBOARD
    # =========================================================
    def dashboard(self):

        return render_template(
            "admin/dashboard.html",

            counts=(
                self.bike_model
                .counts()
            ),

            bikes=(
                self.bike_model
                .get_all()[:5]
            ),

            inquiries=(
                self.inquiry_model
                .get_all_with_bike()[:5]
            ),

            new_inquiries=(
                self.inquiry_model
                .count_new()
            )
        )

    # =========================================================
    # ALL BIKES
    # =========================================================
    def bikes(self):

        bikes = (
            self.bike_model
            .get_all(
                status=(
                    request.args.get(
                        "status"
                    )
                    or None
                ),

                brand=(
                    request.args.get(
                        "brand"
                    )
                    or None
                ),

                search=(
                    request.args.get(
                        "search"
                    )
                    or None
                )
            )
        )

        return render_template(
            "admin/bikes.html",

            bikes=bikes,

            brands=(
                self.bike_model
                .get_brands()
            ),

            new_inquiries=(
                self.inquiry_model
                .count_new()
            )
        )

    # =========================================================
    # IMAGE VALIDATION
    # =========================================================
    def _allowed_image(
        self,
        filename
    ):

        return (
            "." in filename
            and filename
            .rsplit(
                ".",
                1
            )[1]
            .lower()
            in config.ALLOWED_IMAGE_EXTENSIONS
        )

    # =========================================================
    # SAVE IMAGE
    # =========================================================
    def _save_file(
        self,
        file_obj
    ):

        if (
            not file_obj
            or not file_obj.filename
            or not self._allowed_image(
                file_obj.filename
            )
        ):

            return None

        filename = (
            secure_filename(
                file_obj.filename
            )
        )

        filename = (
            f"{int(time.time() * 1000)}_"
            f"{filename}"
        )

        upload_folder = (
            current_app.config[
                "BIKE_UPLOAD_FOLDER"
            ]
        )

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        file_path = os.path.join(
            upload_folder,
            filename
        )

        file_obj.save(
            file_path
        )

        return filename

    # =========================================================
    # CONVERT INTEGER
    # =========================================================
    def _int_or(
        self,
        value,
        default=0
    ):

        try:

            return int(
                value
            )

        except (
            TypeError,
            ValueError
        ):

            return default

    # =========================================================
    # CONVERT FLOAT
    # =========================================================
    def _float_or_none(
        self,
        value
    ):

        try:

            if value in (
                None,
                ""
            ):

                return None

            return float(
                value
            )

        except (
            TypeError,
            ValueError
        ):

            return None

    # =========================================================
    # NORMALIZE DATE
    # =========================================================
    def _date_or_none(
        self,
        value
    ):

        if not value:

            return None

        try:

            return datetime.strptime(
                value,
                "%Y-%m-%d"
            ).date()

        except (
            TypeError,
            ValueError
        ):

            return None

    # =========================================================
    # BIKE FORM DATA
    # =========================================================
    def _form_data(
        self,
        old_cover=None,
        existing_bike=None
    ):

        cover = (
            self._save_file(
                request.files.get(
                    "cover_image"
                )
            )
            or old_cover
        )

        existing_bike = (
            existing_bike
            or {}
        )

        data = {

            "name":
                request.form.get(
                    "name",
                    ""
                ).strip(),

            "brand":
                request.form.get(
                    "brand",
                    ""
                ).strip(),

            "model":
                request.form.get(
                    "model",
                    ""
                ).strip(),

            "category":
                request.form.get(
                    "category",
                    "motorcycle"
                ).strip(),

            "year":
                self._int_or(
                    request.form.get(
                        "year"
                    )
                ),

            "engine_cc":
                self._int_or(
                    request.form.get(
                        "engine_cc"
                    )
                ),

            "km_travelled":
                self._int_or(
                    request.form.get(
                        "km_travelled"
                    )
                ),

            "price":
                self._float_or_none(
                    request.form.get(
                        "price"
                    )
                ) or 0,

            "original_price":
                self._float_or_none(
                    request.form.get(
                        "original_price"
                    )
                ),

            "purchase_price":
                self._float_or_none(
                    request.form.get(
                        "purchase_price"
                    )
                ),

            "purchase_date":
                self._date_or_none(
                    request.form.get(
                        "purchase_date"
                    )
                ),

            "additional_expenses":
                self._float_or_none(
                    request.form.get(
                        "additional_expenses"
                    )
                ) or 0,

            "fuel_type":
                request.form.get(
                    "fuel_type",
                    "Petrol"
                ).strip(),

            "transmission":
                request.form.get(
                    "transmission",
                    ""
                ).strip(),

            "colour":
                request.form.get(
                    "colour",
                    ""
                ).strip(),

            "condition_text":
                request.form.get(
                    "condition_text",
                    ""
                ).strip(),

            "owners":
                self._int_or(
                    request.form.get(
                        "owners"
                    ),
                    1
                ),

            "reg_number":
                request.form.get(
                    "reg_number",
                    ""
                ).strip(),

            "short_description":
                request.form.get(
                    "short_description",
                    ""
                ).strip(),

            "full_description":
                request.form.get(
                    "full_description",
                    ""
                ).strip(),

            "features":
                request.form.get(
                    "features",
                    ""
                ).strip(),

            "known_issues":
                request.form.get(
                    "known_issues",
                    ""
                ).strip(),

            "service_info":
                request.form.get(
                    "service_info",
                    ""
                ).strip(),

            "doc_info":
                request.form.get(
                    "doc_info",
                    ""
                ).strip(),

            "cover_image":
                cover,

            "date_added":
                self._date_or_none(
                    request.form.get(
                        "date_added"
                    )
                )
                or existing_bike.get(
                    "date_added"
                )
                or date.today(),

            "status":
                existing_bike.get(
                    "status",
                    "available"
                ),

            "sold_price":
                existing_bike.get(
                    "sold_price"
                ),

            "sold_date":
                existing_bike.get(
                    "sold_date"
                )
        }

        return data

    # =========================================================
    # ADD BIKE
    # =========================================================
    def add_bike(self):

        if request.method == "POST":

            data = self._form_data()

            data["status"] = (
                "available"
            )

            if (
                not data["name"]
                or not data["brand"]
                or not data["model"]
                or data["price"] <= 0
            ):

                flash(
                    "Name, brand, model and "
                    "price are required.",
                    "danger"
                )

                return render_template(
                    "admin/bike_form.html",

                    bike=data,

                    mode="add",

                    new_inquiries=(
                        self.inquiry_model
                        .count_new()
                    )
                )

            if (
                data["purchase_price"]
                is not None
                and data["purchase_price"] < 0
            ):

                flash(
                    "Purchase price cannot "
                    "be negative.",
                    "danger"
                )

                return render_template(
                    "admin/bike_form.html",

                    bike=data,

                    mode="add",

                    new_inquiries=(
                        self.inquiry_model
                        .count_new()
                    )
                )

            bike_id = (
                self.bike_model
                .save(
                    data
                )
            )

            gallery_files = (
                request.files
                .getlist(
                    "gallery_images"
                )
            )

            for (
                index,
                file_obj
            ) in enumerate(
                gallery_files
            ):

                filename = (
                    self._save_file(
                        file_obj
                    )
                )

                if filename:

                    self.bike_model.add_image(
                        bike_id,
                        filename,
                        index
                    )

            flash(
                "Bike added successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "admin.bikes"
                )
            )

        return render_template(
            "admin/bike_form.html",

            bike=None,

            mode="add",

            new_inquiries=(
                self.inquiry_model
                .count_new()
            )
        )

    # =========================================================
    # EDIT BIKE
    # =========================================================
    def edit_bike(
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

            flash(
                "Bike not found.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.bikes"
                )
            )

        if request.method == "POST":

            data = self._form_data(
                old_cover=(
                    bike.get(
                        "cover_image"
                    )
                ),
                existing_bike=bike
            )

            if (
                not data["name"]
                or not data["brand"]
                or not data["model"]
                or data["price"] <= 0
            ):

                flash(
                    "Name, brand, model and "
                    "price are required.",
                    "danger"
                )

                data["images"] = (
                    self.bike_model
                    .get_images(
                        bike_id
                    )
                )

                return render_template(
                    "admin/bike_form.html",

                    bike=data,

                    mode="edit",

                    new_inquiries=(
                        self.inquiry_model
                        .count_new()
                    )
                )

            self.bike_model.update(
                bike_id,
                data
            )

            new_gallery = (
                request.files
                .getlist(
                    "gallery_images"
                )
            )

            if any(
                file_obj
                and file_obj.filename

                for file_obj
                in new_gallery
            ):

                self.bike_model.clear_images(
                    bike_id
                )

                for (
                    index,
                    file_obj
                ) in enumerate(
                    new_gallery
                ):

                    filename = (
                        self._save_file(
                            file_obj
                        )
                    )

                    if filename:

                        self.bike_model.add_image(
                            bike_id,
                            filename,
                            index
                        )

            flash(
                "Bike updated successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "admin.bikes"
                )
            )

        bike["images"] = (
            self.bike_model
            .get_images(
                bike_id
            )
        )

        return render_template(
            "admin/bike_form.html",

            bike=bike,

            mode="edit",

            new_inquiries=(
                self.inquiry_model
                .count_new()
            )
        )

    # =========================================================
    # DELETE BIKE
    # =========================================================
    def delete_bike(
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

            flash(
                "Bike not found.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.bikes"
                )
            )

        if (
            bike.get(
                "status"
            )
            == "sold"
        ):

            flash(
                "Sold bikes cannot be deleted "
                "because they are part of the "
                "sales history.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.bikes"
                )
            )

        self.bike_model.delete_by_id(
            bike_id
        )

        flash(
            "Bike deleted successfully.",
            "success"
        )

        return redirect(
            url_for(
                "admin.bikes"
            )
        )

    # =========================================================
    # TOGGLE BIKE STATUS
    # =========================================================
    def toggle_bike_status(
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

            flash(
                "Bike not found.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.bikes"
                )
            )

        if (
            bike.get(
                "status"
            )
            == "available"
        ):

            return redirect(
                url_for(
                    "admin.mark_bike_sold",
                    bike_id=bike_id
                )
            )

        if (
            bike.get(
                "status"
            )
            == "sold"
        ):

            self.bike_model.mark_as_available(
                bike_id
            )

            flash(
                "Bike returned to available "
                "inventory. Its sale record "
                "was removed from sales history.",
                "success"
            )

            return redirect(
                url_for(
                    "admin.bikes"
                )
            )

        flash(
            "This bike cannot be toggled "
            "from its current status.",
            "danger"
        )

        return redirect(
            url_for(
                "admin.bikes"
            )
        )

    # =========================================================
    # MARK BIKE AS SOLD
    # =========================================================
    def mark_bike_sold(
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

            flash(
                "Bike not found.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.bikes"
                )
            )

        if (
            bike.get(
                "status"
            )
            == "sold"
            and request.method
            == "GET"
        ):

            flash(
                "This bike is already sold.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.sales"
                )
            )

        if request.method == "POST":

            sold_price = (
                self._float_or_none(
                    request.form.get(
                        "sold_price"
                    )
                )
            )

            sold_date = (
                self._date_or_none(
                    request.form.get(
                        "sold_date"
                    )
                )
            )

            purchase_price = (
                self._float_or_none(
                    request.form.get(
                        "purchase_price"
                    )
                )
            )

            purchase_date = (
                self._date_or_none(
                    request.form.get(
                        "purchase_date"
                    )
                )
            )

            additional_expenses = (
                self._float_or_none(
                    request.form.get(
                        "additional_expenses"
                    )
                )
            )

            if additional_expenses is None:

                additional_expenses = 0

            if (
                sold_price is None
                or sold_price <= 0
            ):

                flash(
                    "Please enter a valid "
                    "sold price.",
                    "danger"
                )

                return render_template(
                    "admin/mark_sold.html",

                    bike=bike,

                    today=date.today(),

                    new_inquiries=(
                        self.inquiry_model
                        .count_new()
                    )
                )

            if sold_date is None:

                flash(
                    "Please select the "
                    "sold date.",
                    "danger"
                )

                return render_template(
                    "admin/mark_sold.html",

                    bike=bike,

                    today=date.today(),

                    new_inquiries=(
                        self.inquiry_model
                        .count_new()
                    )
                )

            if purchase_price is None:

                purchase_price = (
                    bike.get(
                        "purchase_price"
                    )
                )

            if purchase_date is None:

                purchase_date = (
                    bike.get(
                        "purchase_date"
                    )
                )

            if (
                purchase_price is None
                or float(
                    purchase_price
                ) <= 0
            ):

                flash(
                    "Purchase price is required "
                    "before the bike can be "
                    "marked as sold.",
                    "danger"
                )

                return render_template(
                    "admin/mark_sold.html",

                    bike=bike,

                    today=date.today(),

                    new_inquiries=(
                        self.inquiry_model
                        .count_new()
                    )
                )

            if additional_expenses < 0:

                flash(
                    "Additional expenses cannot "
                    "be negative.",
                    "danger"
                )

                return render_template(
                    "admin/mark_sold.html",

                    bike=bike,

                    today=date.today(),

                    new_inquiries=(
                        self.inquiry_model
                        .count_new()
                    )
                )

            if (
                purchase_date
                and sold_date
                < purchase_date
            ):

                flash(
                    "Sold date cannot be earlier "
                    "than the purchase date.",
                    "danger"
                )

                return render_template(
                    "admin/mark_sold.html",

                    bike=bike,

                    today=date.today(),

                    new_inquiries=(
                        self.inquiry_model
                        .count_new()
                    )
                )

            self.bike_model.mark_as_sold(
                bike_id=bike_id,
                sold_price=sold_price,
                sold_date=sold_date,
                purchase_price=purchase_price,
                purchase_date=purchase_date,
                additional_expenses=(
                    additional_expenses
                )
            )

            net_profit = (
                float(
                    sold_price
                )
                - float(
                    purchase_price
                )
                - float(
                    additional_expenses
                )
            )

            flash(
                (
                    "Bike marked as sold "
                    "successfully. "
                    f"Net profit: "
                    f"Rs. {net_profit:,.2f}"
                ),
                "success"
            )

            return redirect(
                url_for(
                    "admin.sales",
                    month=(
                        sold_date.month
                    ),
                    year=(
                        sold_date.year
                    )
                )
            )

        return render_template(
            "admin/mark_sold.html",

            bike=bike,

            today=date.today(),

            new_inquiries=(
                self.inquiry_model
                .count_new()
            )
        )

    # =========================================================
    # INQUIRIES
    # =========================================================
    def inquiries(self):

        return render_template(
            "admin/inquiries.html",

            inquiries=(
                self.inquiry_model
                .get_all_with_bike()
            ),

            new_inquiries=(
                self.inquiry_model
                .count_new()
            )
        )

    # =========================================================
    # UPDATE INQUIRY
    # =========================================================
    def update_inquiry(
        self,
        inquiry_id
    ):

        status = request.form.get(
            "status",
            "new"
        )

        allowed_statuses = {
            "new",
            "contacted",
            "closed"
        }

        if (
            status
            not in allowed_statuses
        ):

            flash(
                "Invalid inquiry status.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.inquiries"
                )
            )

        self.inquiry_model.update_status(
            inquiry_id,
            status
        )

        flash(
            "Inquiry status updated.",
            "success"
        )

        return redirect(
            url_for(
                "admin.inquiries"
            )
        )

    # =========================================================
    # SETTINGS
    # =========================================================
    def settings(self):

        settings = (
            self.settings_model
            .get()
            or {}
        )

        if request.method == "POST":

            data = dict(
                settings
            )

            # =================================================
            # BUSINESS NAME
            # =================================================
            business_name = (
                request.form.get(
                    "business_name",
                    ""
                )
                .strip()
            )

            if not business_name:

                flash(
                    "Business name is required.",
                    "danger"
                )

                return render_template(
                    "admin/settings.html",

                    settings=data,

                    new_inquiries=(
                        self.inquiry_model
                        .count_new()
                    )
                )

            if len(
                business_name
            ) > 120:

                flash(
                    "Business name cannot exceed "
                    "120 characters.",
                    "danger"
                )

                return render_template(
                    "admin/settings.html",

                    settings=data,

                    new_inquiries=(
                        self.inquiry_model
                        .count_new()
                    )
                )

            # =================================================
            # PHONE
            # =================================================
            phone = (
                request.form.get(
                    "phone",
                    ""
                )
                .strip()
            )

            if len(
                phone
            ) > 40:

                flash(
                    "Phone number is too long.",
                    "danger"
                )

                return render_template(
                    "admin/settings.html",

                    settings=data,

                    new_inquiries=(
                        self.inquiry_model
                        .count_new()
                    )
                )

            # =================================================
            # EMAIL
            # =================================================
            email = (
                request.form.get(
                    "email",
                    ""
                )
                .strip()
                .lower()
            )

            if len(
                email
            ) > 150:

                flash(
                    "Email address is too long.",
                    "danger"
                )

                return render_template(
                    "admin/settings.html",

                    settings=data,

                    new_inquiries=(
                        self.inquiry_model
                        .count_new()
                    )
                )

            # =================================================
            # ADDRESS
            # =================================================
            address = (
                request.form.get(
                    "address",
                    ""
                )
                .strip()
            )

            if len(
                address
            ) > 255:

                flash(
                    "Address cannot exceed "
                    "255 characters.",
                    "danger"
                )

                return render_template(
                    "admin/settings.html",

                    settings=data,

                    new_inquiries=(
                        self.inquiry_model
                        .count_new()
                    )
                )

            # =================================================
            # OPENING HOURS
            # =================================================
            opening_hours = (
                request.form.get(
                    "opening_hours",
                    ""
                )
                .strip()
            )

            if len(
                opening_hours
            ) > 500:

                flash(
                    "Opening hours cannot exceed "
                    "500 characters.",
                    "danger"
                )

                return render_template(
                    "admin/settings.html",

                    settings=data,

                    new_inquiries=(
                        self.inquiry_model
                        .count_new()
                    )
                )

            # =================================================
            # ABOUT CONTENT
            # =================================================
            about_content = (
                request.form.get(
                    "about_content",
                    ""
                )
                .strip()
            )

            if len(
                about_content
            ) > 5000:

                flash(
                    "About content cannot exceed "
                    "5000 characters.",
                    "danger"
                )

                return render_template(
                    "admin/settings.html",

                    settings=data,

                    new_inquiries=(
                        self.inquiry_model
                        .count_new()
                    )
                )

            # =================================================
            # UPDATE CLEAN DATA
            # =================================================
            data.update({

                "business_name":
                    business_name,

                "phone":
                    phone,

                "email":
                    email or None,

                "address":
                    address,

                "opening_hours":
                    opening_hours,

                "about_content":
                    about_content,

                # No social media handles currently
                "tiktok":
                    None,

                "facebook":
                    None,

                "instagram":
                    None
            })

            # =================================================
            # LOGO
            # =================================================
            logo = (
                request.files.get(
                    "logo"
                )
            )

            if (
                logo
                and logo.filename
            ):

                filename = (
                    self._save_file(
                        logo
                    )
                )

                if not filename:

                    flash(
                        "Invalid logo image.",
                        "danger"
                    )

                    return render_template(
                        "admin/settings.html",

                        settings=data,

                        new_inquiries=(
                            self.inquiry_model
                            .count_new()
                        )
                    )

                data["logo"] = (
                    "uploads/bikes/"
                    + filename
                )

            # =================================================
            # SAVE
            # =================================================
            self.settings_model.update(
                data
            )

            flash(
                "Settings saved successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "admin.settings"
                )
            )

        return render_template(
            "admin/settings.html",

            settings=settings,

            new_inquiries=(
                self.inquiry_model
                .count_new()
            )
        )

    # =========================================================
    # SALES & PROFIT
    # =========================================================
    def sales(self):

        today = (
            datetime.now()
        )

        selected_month = (
            request.args.get(
                "month",
                default=(
                    today.month
                ),
                type=int
            )
        )

        selected_year = (
            request.args.get(
                "year",
                default=(
                    today.year
                ),
                type=int
            )
        )

        if (
            selected_month < 1
            or selected_month > 12
        ):

            selected_month = (
                today.month
            )

        summary = (
            self.bike_model
            .get_monthly_profit(
                selected_year,
                selected_month
            )
        )

        sales = (
            self.bike_model
            .get_sales_report(
                year=(
                    selected_year
                ),
                month=(
                    selected_month
                )
            )
        )

        months = [
            (1, "January"),
            (2, "February"),
            (3, "March"),
            (4, "April"),
            (5, "May"),
            (6, "June"),
            (7, "July"),
            (8, "August"),
            (9, "September"),
            (10, "October"),
            (11, "November"),
            (12, "December")
        ]

        years = list(
            range(
                today.year,
                today.year - 10,
                -1
            )
        )

        return render_template(
            "admin/sales.html",

            sales=sales,

            summary=summary,

            months=months,

            years=years,

            selected_month=(
                selected_month
            ),

            selected_year=(
                selected_year
            ),

            new_inquiries=(
                self.inquiry_model
                .count_new()
            )
        )

    # =========================================================
    # EXPORT SALES CSV
    # =========================================================
    def export_sales_csv(self):

        selected_month = (
            request.args.get(
                "month",
                default=None,
                type=int
            )
        )

        selected_year = (
            request.args.get(
                "year",
                default=None,
                type=int
            )
        )

        sales = (
            self.bike_model
            .get_sales_report(
                year=(
                    selected_year
                ),
                month=(
                    selected_month
                )
            )
        )

        output = (
            io.StringIO()
        )

        writer = (
            csv.writer(
                output
            )
        )

        writer.writerow([
            "Bike ID",
            "Bike Name",
            "Brand",
            "Model",
            "Purchase Date",
            "Purchase Price",
            "Sold Date",
            "Sold Price",
            "Additional Expenses",
            "Gross Profit",
            "Net Profit"
        ])

        for bike in sales:

            writer.writerow([
                bike.get(
                    "id"
                ),

                bike.get(
                    "name"
                ),

                bike.get(
                    "brand"
                ),

                bike.get(
                    "model"
                ),

                bike.get(
                    "purchase_date"
                ),

                bike.get(
                    "purchase_price"
                ),

                bike.get(
                    "sold_date"
                ),

                bike.get(
                    "sold_price"
                ),

                bike.get(
                    "additional_expenses"
                ),

                bike.get(
                    "gross_profit"
                ),

                bike.get(
                    "net_profit"
                )
            ])

        filename = (
            "supa_auto_link_"
            "sales_report"
        )

        if selected_year:

            filename += (
                f"_{selected_year}"
            )

        if selected_month:

            filename += (
                f"_{selected_month:02d}"
            )

        filename += (
            ".csv"
        )

        response = Response(
            output.getvalue(),
            mimetype=(
                "text/csv; "
                "charset=utf-8"
            )
        )

        response.headers[
            "Content-Disposition"
        ] = (
            "attachment; "
            f"filename={filename}"
        )

        return response