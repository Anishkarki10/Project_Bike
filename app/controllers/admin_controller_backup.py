import os
import csv
import io
import uuid
import re

from datetime import datetime, date
from urllib.parse import urlparse

from PIL import Image, UnidentifiedImageError

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

    def __init__(self):
        self.user_model = User()
        self.bike_model = Bike()
        self.inquiry_model = Inquiry()
        self.settings_model = Settings()

    # Every controller/helper method must be indented
    # inside this class.

    def _clean_text(
        self,
        value,
        maximum_length,
        required=False,
        field_name="Field"
    ):
        value = (value or "").strip()

        if required and not value:
            raise ValueError(
                f"{field_name} is required."
            )

        if len(value) > maximum_length:
            raise ValueError(
                f"{field_name} cannot exceed "
                f"{maximum_length} characters."
            )

        return value