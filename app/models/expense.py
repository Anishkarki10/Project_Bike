from app.models.base_model import BaseModel
from app.models.database import Database


class Expense(BaseModel):

    # =========================================================
    # BASE MODEL TABLE
    # =========================================================
    @property
    def table(self):
        return "expenses"

    # =========================================================
    # GET EXPENSES (optionally filtered by month/year)
    # =========================================================
    def get_all(
        self,
        year=None,
        month=None
    ):
        sql = """
            SELECT *
            FROM expenses
            WHERE 1 = 1
        """

        params = []

        if year:
            sql += " AND YEAR(expense_date) = %s"
            params.append(year)

        if month:
            sql += " AND MONTH(expense_date) = %s"
            params.append(month)

        sql += " ORDER BY expense_date DESC, id DESC"

        db = Database()

        rows = db.fetch_all(
            sql,
            tuple(params)
        )

        db.close()

        return rows

    # =========================================================
    # MONTHLY EXPENSE TOTAL
    # =========================================================
    def get_monthly_total(
        self,
        year,
        month
    ):
        db = Database()

        result = db.fetch_one(
            """
            SELECT COALESCE(SUM(amount), 0) AS total

            FROM expenses

            WHERE YEAR(expense_date) = %s
            AND MONTH(expense_date) = %s
            """,
            (
                year,
                month
            )
        )

        db.close()

        return result["total"]

    # =========================================================
    # ADD EXPENSE
    # =========================================================
    def save(self, data):

        db = Database()

        expense_id = db.execute(
            """
            INSERT INTO expenses
            (
                title,
                category,
                amount,
                expense_date,
                notes
            )
            VALUES
            (
                %s, %s, %s, %s, %s
            )
            """,
            (
                data["title"],

                data.get(
                    "category",
                    "other"
                ),

                data["amount"],

                data["expense_date"],

                data.get("notes")
            )
        )

        db.close()

        return expense_id
