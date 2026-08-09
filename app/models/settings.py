from app.models.database import Database


class Settings:

    # =========================================================
    # GET SETTINGS
    # =========================================================
    def get(self):

        db = Database()

        row = db.fetch_one(
            """
            SELECT *
            FROM settings
            WHERE id = 1
            """
        )

        db.close()

        return row

    # =========================================================
    # UPDATE SETTINGS
    # =========================================================
    def update(
        self,
        data
    ):

        allowed_fields = {
            "business_name",
            "phone",
            "email",
            "address",
            "opening_hours",
            "tiktok",
            "facebook",
            "instagram",
            "about_content",
            "logo"
        }

        # Defensive check:
        # reject unexpected keys instead of silently accepting
        # a malformed settings dictionary.
        unexpected_fields = (
            set(data.keys())
            - allowed_fields
        )

        if unexpected_fields:

            raise ValueError(
                "Unexpected settings fields: "
                + ", ".join(
                    sorted(
                        unexpected_fields
                    )
                )
            )

        db = Database()

        db.execute(
            """
            UPDATE settings

            SET
                business_name = %s,
                phone = %s,
                email = %s,
                address = %s,
                opening_hours = %s,
                tiktok = %s,
                facebook = %s,
                instagram = %s,
                about_content = %s,
                logo = %s

            WHERE id = 1
            """,
            (
                data.get(
                    "business_name"
                ),

                data.get(
                    "phone"
                ),

                data.get(
                    "email"
                ),

                data.get(
                    "address"
                ),

                data.get(
                    "opening_hours"
                ),

                data.get(
                    "tiktok"
                ),

                data.get(
                    "facebook"
                ),

                data.get(
                    "instagram"
                ),

                data.get(
                    "about_content"
                ),

                data.get(
                    "logo"
                )
            )
        )

        db.close()