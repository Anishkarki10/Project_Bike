from abc import ABC, abstractmethod

from app.models.database import Database


class BaseModel(ABC):

    # =========================================================
    # TABLE NAME
    # =========================================================
    @property
    @abstractmethod
    def table(self):
        pass

    # =========================================================
    # ALLOWED SORT COLUMNS
    # =========================================================
    ALLOWED_ORDER_COLUMNS = {
        "id",
        "created_at",
        "name"
    }

    # =========================================================
    # FIND ONE RECORD BY ID
    # =========================================================
    def find_by_id(
        self,
        record_id
    ):

        try:
            record_id = int(
                record_id
            )

        except (
            TypeError,
            ValueError
        ):
            return None

        if record_id <= 0:
            return None

        db = Database()

        result = db.fetch_one(
            f"""
            SELECT *
            FROM `{self.table}`
            WHERE id = %s
            """,
            (
                record_id,
            )
        )

        db.close()

        return result

    # =========================================================
    # FIND ALL RECORDS
    # =========================================================
    def find_all(
        self,
        order_by="id",
        direction="DESC"
    ):

        # -----------------------------------------------------
        # Never allow arbitrary ORDER BY SQL.
        # -----------------------------------------------------
        if (
            order_by
            not in self.ALLOWED_ORDER_COLUMNS
        ):
            order_by = "id"

        direction = (
            str(direction)
            .upper()
        )

        if direction not in {
            "ASC",
            "DESC"
        }:
            direction = "DESC"

        db = Database()

        result = db.fetch_all(
            f"""
            SELECT *
            FROM `{self.table}`
            ORDER BY `{order_by}` {direction}
            """
        )

        db.close()

        return result

    # =========================================================
    # DELETE RECORD BY ID
    # =========================================================
    def delete_by_id(
        self,
        record_id
    ):

        try:
            record_id = int(
                record_id
            )

        except (
            TypeError,
            ValueError
        ):
            return False

        if record_id <= 0:
            return False

        db = Database()

        db.execute(
            f"""
            DELETE FROM `{self.table}`
            WHERE id = %s
            """,
            (
                record_id,
            )
        )

        db.close()

        return True