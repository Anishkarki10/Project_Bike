from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.models.base_model import BaseModel
from app.models.database import Database


class User(BaseModel):

    # =========================================================
    # TABLE NAME
    # =========================================================
    @property
    def table(self):

        return "users"

    # =========================================================
    # FIND USER BY EMAIL
    # =========================================================
    def find_by_email(
        self,
        email
    ):

        email = (
            email
            or ""
        ).strip().lower()

        if not email:
            return None

        if len(email) > 150:
            return None

        db = Database()

        row = db.fetch_one(
            """
            SELECT *
            FROM users
            WHERE email = %s
            LIMIT 1
            """,
            (
                email,
            )
        )

        db.close()

        return row

    # =========================================================
    # CHECK PASSWORD
    # =========================================================
    def check_password(
        self,
        hashed_password,
        plain_password
    ):

        if not hashed_password:
            return False

        if not plain_password:
            return False

        try:

            return check_password_hash(
                hashed_password,
                plain_password
            )

        except (
            ValueError,
            TypeError
        ):

            return False

    # =========================================================
    # UPDATE PASSWORD
    # =========================================================
    def update_password(
        self,
        user_id,
        plain_password
    ):

        try:

            user_id = int(
                user_id
            )

        except (
            TypeError,
            ValueError
        ):

            return False

        if user_id <= 0:
            return False

        if not plain_password:
            return False

        # -----------------------------------------------------
        # BASIC PASSWORD POLICY
        # -----------------------------------------------------
        if len(plain_password) < 12:

            raise ValueError(
                "Password must contain at least 12 characters."
            )

        if len(plain_password) > 255:

            raise ValueError(
                "Password is too long."
            )

        password_hash = (
            generate_password_hash(
                plain_password
            )
        )

        db = Database()

        db.execute(
            """
            UPDATE users
            SET password = %s
            WHERE id = %s
            """,
            (
                password_hash,
                user_id
            )
        )

        db.close()

        return True