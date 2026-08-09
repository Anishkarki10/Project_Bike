from app.models.base_model import BaseModel
from app.models.database import Database


class Inquiry(BaseModel):

    # =========================================================
    # TABLE NAME
    # =========================================================
    @property
    def table(self):

        return "inquiries"

    # =========================================================
    # CREATE INQUIRY
    # =========================================================
    def create(
        self,
        data
    ):

        db = Database()

        db.execute(
            """
            INSERT INTO inquiries
            (
                name,
                phone,
                email,
                bike_id,
                bike_interested,
                message,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                'new'
            )
            """,
            (
                data["name"],
                data["phone"],
                data.get("email"),
                data.get("bike_id"),
                data.get("bike_interested"),
                data["message"]
            )
        )

        db.close()

    # =========================================================
    # GET ALL INQUIRIES WITH BIKE
    # =========================================================
    def get_all_with_bike(
        self
    ):

        db = Database()

        rows = db.fetch_all(
            """
            SELECT
                inquiries.*,
                bikes.name AS bike_name

            FROM inquiries

            LEFT JOIN bikes
                ON inquiries.bike_id = bikes.id

            ORDER BY
                inquiries.id DESC
            """
        )

        db.close()

        return rows

    # =========================================================
    # UPDATE INQUIRY STATUS
    # =========================================================
    def update_status(
        self,
        inquiry_id,
        status
    ):

        allowed_statuses = {
            "new",
            "contacted",
            "closed"
        }

        if status not in allowed_statuses:

            raise ValueError(
                "Invalid inquiry status."
            )

        db = Database()

        db.execute(
            """
            UPDATE inquiries

            SET status = %s

            WHERE id = %s
            """,
            (
                status,
                inquiry_id
            )
        )

        db.close()

    # =========================================================
    # COUNT NEW INQUIRIES
    # =========================================================
    def count_new(
        self
    ):

        db = Database()

        result = db.fetch_one(
            """
            SELECT
                COUNT(*) AS total

            FROM inquiries

            WHERE status = 'new'
            """
        )

        db.close()

        return (
            result["total"]
            if result
            else 0
        )