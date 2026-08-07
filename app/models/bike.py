from app.models.base_model import BaseModel
from app.models.database import Database


class Bike(BaseModel):

    # =========================================================
    # BASE MODEL TABLE
    # =========================================================
    @property
    def table(self):
        return "bikes"

    # =========================================================
    # GET ALL BIKES
    # =========================================================
    def get_all(
        self,
        status=None,
        brand=None,
        category=None,
        min_price=None,
        max_price=None,
        search=None
    ):
        sql = """
            SELECT *
            FROM bikes
            WHERE 1 = 1
        """

        params = []

        if status:
            sql += " AND status = %s"
            params.append(status)

        if brand:
            sql += " AND brand = %s"
            params.append(brand)

        if category:
            sql += " AND category = %s"
            params.append(category)

        if min_price:
            sql += " AND price >= %s"
            params.append(min_price)

        if max_price:
            sql += " AND price <= %s"
            params.append(max_price)

        if search:
            sql += """
                AND (
                    name LIKE %s
                    OR brand LIKE %s
                    OR model LIKE %s
                )
            """

            term = f"%{search}%"

            params.extend([
                term,
                term,
                term
            ])

        sql += " ORDER BY id DESC"

        db = Database()

        rows = db.fetch_all(
            sql,
            tuple(params)
        )

        db.close()

        return rows

    # =========================================================
    # FEATURED AVAILABLE BIKES
    # =========================================================
    def get_available_featured(self, limit=6):

        db = Database()

        rows = db.fetch_all(
            """
            SELECT *
            FROM bikes
            WHERE status = 'available'
            ORDER BY id DESC
            LIMIT %s
            """,
            (limit,)
        )

        db.close()

        return rows

    # =========================================================
    # GET BRANDS
    # =========================================================
    def get_brands(self):

        db = Database()

        rows = db.fetch_all(
            """
            SELECT DISTINCT brand
            FROM bikes
            WHERE brand IS NOT NULL
            AND brand != ''
            ORDER BY brand
            """
        )

        db.close()

        return [
            row["brand"]
            for row in rows
        ]

    # =========================================================
    # GET BIKE IMAGES
    # =========================================================
    def get_images(self, bike_id):

        db = Database()

        rows = db.fetch_all(
            """
            SELECT *
            FROM bike_images
            WHERE bike_id = %s
            ORDER BY sort_order, id
            """,
            (bike_id,)
        )

        db.close()

        return [
            row["image_path"]
            for row in rows
        ]

    # =========================================================
    # ADD BIKE
    # =========================================================
    def save(self, data):

        db = Database()

        bike_id = db.execute(
            """
            INSERT INTO bikes
            (
                name,
                brand,
                model,
                category,
                year,
                engine_cc,
                km_travelled,

                price,
                original_price,

                purchase_price,
                purchase_date,

                sold_price,
                sold_date,

                additional_expenses,

                fuel_type,
                transmission,
                colour,
                condition_text,
                owners,
                reg_number,

                short_description,
                full_description,
                features,
                known_issues,
                service_info,
                doc_info,

                status,
                cover_image,
                date_added
            )
            VALUES
            (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            """,
            (
                data["name"],
                data["brand"],
                data["model"],
                data["category"],
                data["year"],
                data["engine_cc"],
                data["km_travelled"],

                data["price"],
                data.get("original_price"),

                data.get("purchase_price"),
                data.get("purchase_date"),

                data.get("sold_price"),
                data.get("sold_date"),

                data.get(
                    "additional_expenses",
                    0
                ),

                data.get(
                    "fuel_type",
                    "Petrol"
                ),

                data.get(
                    "transmission"
                ),

                data.get(
                    "colour"
                ),

                data.get(
                    "condition_text"
                ),

                data.get(
                    "owners",
                    1
                ),

                data.get(
                    "reg_number"
                ),

                data.get(
                    "short_description"
                ),

                data.get(
                    "full_description"
                ),

                data.get(
                    "features"
                ),

                data.get(
                    "known_issues"
                ),

                data.get(
                    "service_info"
                ),

                data.get(
                    "doc_info"
                ),

                data.get(
                    "status",
                    "available"
                ),

                data.get(
                    "cover_image"
                ),

                data.get(
                    "date_added"
                )
            )
        )

        db.close()

        return bike_id

    # =========================================================
    # UPDATE BIKE
    # =========================================================
    def update(self, bike_id, data):

        db = Database()

        db.execute(
            """
            UPDATE bikes

            SET
                name = %s,
                brand = %s,
                model = %s,
                category = %s,

                year = %s,
                engine_cc = %s,
                km_travelled = %s,

                price = %s,
                original_price = %s,

                purchase_price = %s,
                purchase_date = %s,

                additional_expenses = %s,

                fuel_type = %s,
                transmission = %s,
                colour = %s,
                condition_text = %s,

                owners = %s,
                reg_number = %s,

                short_description = %s,
                full_description = %s,

                features = %s,
                known_issues = %s,
                service_info = %s,
                doc_info = %s,

                cover_image = %s,
                date_added = %s

            WHERE id = %s
            """,
            (
                data["name"],
                data["brand"],
                data["model"],
                data["category"],

                data["year"],
                data["engine_cc"],
                data["km_travelled"],

                data["price"],
                data.get(
                    "original_price"
                ),

                data.get(
                    "purchase_price"
                ),

                data.get(
                    "purchase_date"
                ),

                data.get(
                    "additional_expenses",
                    0
                ),

                data.get(
                    "fuel_type"
                ),

                data.get(
                    "transmission"
                ),

                data.get(
                    "colour"
                ),

                data.get(
                    "condition_text"
                ),

                data.get(
                    "owners",
                    1
                ),

                data.get(
                    "reg_number"
                ),

                data.get(
                    "short_description"
                ),

                data.get(
                    "full_description"
                ),

                data.get(
                    "features"
                ),

                data.get(
                    "known_issues"
                ),

                data.get(
                    "service_info"
                ),

                data.get(
                    "doc_info"
                ),

                data.get(
                    "cover_image"
                ),

                data.get(
                    "date_added"
                ),

                bike_id
            )
        )

        db.close()

    # =========================================================
    # ADD GALLERY IMAGE
    # =========================================================
    def add_image(
        self,
        bike_id,
        image_path,
        sort_order=0
    ):

        db = Database()

        db.execute(
            """
            INSERT INTO bike_images
            (
                bike_id,
                image_path,
                sort_order
            )
            VALUES (%s, %s, %s)
            """,
            (
                bike_id,
                image_path,
                sort_order
            )
        )

        db.close()

    # =========================================================
    # REMOVE ALL GALLERY IMAGES
    # =========================================================
    def clear_images(self, bike_id):

        db = Database()

        db.execute(
            """
            DELETE FROM bike_images
            WHERE bike_id = %s
            """,
            (bike_id,)
        )

        db.close()

    # =========================================================
    # DELETE BIKE
    # =========================================================
    def delete_by_id(self, bike_id):

        db = Database()

        db.execute(
            """
            DELETE FROM bikes
            WHERE id = %s
            """,
            (bike_id,)
        )

        db.close()

    # =========================================================
    # MARK BIKE AS SOLD
    # =========================================================
    def mark_as_sold(
        self,
        bike_id,
        sold_price,
        sold_date,
        purchase_price=None,
        purchase_date=None,
        additional_expenses=0
    ):
        """
        Complete a bike sale.

        Profit is NOT stored as a separate database value.

        It is calculated from:
        sold_price
        - purchase_price
        - additional_expenses

        This avoids inconsistent profit values.
        """

        db = Database()

        db.execute(
            """
            UPDATE bikes

            SET
                status = 'sold',

                sold_price = %s,
                sold_date = %s,

                purchase_price =
                    COALESCE(
                        %s,
                        purchase_price
                    ),

                purchase_date =
                    COALESCE(
                        %s,
                        purchase_date
                    ),

                additional_expenses = %s

            WHERE id = %s
            """,
            (
                sold_price,
                sold_date,

                purchase_price,
                purchase_date,

                additional_expenses,

                bike_id
            )
        )

        db.close()

    # =========================================================
    # RETURN SOLD BIKE TO AVAILABLE
    # =========================================================
    def mark_as_available(self, bike_id):
        """
        If a sale was entered accidentally,
        return the bike to available inventory.

        Sale information is cleared so it will
        disappear from sales reports.
        """

        db = Database()

        db.execute(
            """
            UPDATE bikes

            SET
                status = 'available',
                sold_price = NULL,
                sold_date = NULL

            WHERE id = %s
            """,
            (bike_id,)
        )

        db.close()

    # =========================================================
    # STATUS TOGGLE
    # =========================================================
    def toggle_status(self, bike_id):
        """
        IMPORTANT:

        Available -> Sold should NOT happen here.

        Selling requires:
        - sold price
        - sold date
        - purchase price
        - expenses

        Therefore the controller should open
        the Mark as Sold form for available bikes.

        This method is only useful for changing
        a SOLD bike back to AVAILABLE.
        """

        bike = self.find_by_id(
            bike_id
        )

        if not bike:
            return False

        if bike.get("status") == "sold":

            self.mark_as_available(
                bike_id
            )

            return "available"

        return "requires_sale_details"

    # =========================================================
    # COUNTS
    # =========================================================
    def counts(self):

        db = Database()

        total = db.fetch_one(
            """
            SELECT COUNT(*) AS total
            FROM bikes
            """
        )["total"]

        available = db.fetch_one(
            """
            SELECT COUNT(*) AS total
            FROM bikes
            WHERE status = 'available'
            """
        )["total"]

        sold = db.fetch_one(
            """
            SELECT COUNT(*) AS total
            FROM bikes
            WHERE status = 'sold'
            """
        )["total"]

        draft = db.fetch_one(
            """
            SELECT COUNT(*) AS total
            FROM bikes
            WHERE status = 'draft'
            """
        )["total"]

        db.close()

        return {
            "total": total,
            "available": available,
            "sold": sold,
            "draft": draft
        }

    # =========================================================
    # SALES HISTORY
    # =========================================================
    def get_sales_report(
        self,
        year=None,
        month=None
    ):

        sql = """
            SELECT
                id,
                name,
                brand,
                model,
                category,

                year,
                engine_cc,
                km_travelled,

                purchase_price,
                purchase_date,

                sold_price,
                sold_date,

                additional_expenses,

                (
                    COALESCE(
                        sold_price,
                        0
                    )
                    -
                    COALESCE(
                        purchase_price,
                        0
                    )
                ) AS gross_profit,

                (
                    COALESCE(
                        sold_price,
                        0
                    )
                    -
                    COALESCE(
                        purchase_price,
                        0
                    )
                    -
                    COALESCE(
                        additional_expenses,
                        0
                    )
                ) AS net_profit,

                cover_image

            FROM bikes

            WHERE status = 'sold'
            AND sold_price IS NOT NULL
            AND sold_date IS NOT NULL
        """

        params = []

        if year:
            sql += """
                AND YEAR(sold_date) = %s
            """

            params.append(year)

        if month:
            sql += """
                AND MONTH(sold_date) = %s
            """

            params.append(month)

        sql += """
            ORDER BY sold_date DESC, id DESC
        """

        db = Database()

        sales = db.fetch_all(
            sql,
            tuple(params)
        )

        db.close()

        return sales

    # =========================================================
    # SINGLE SALE RECORD
    # =========================================================
    def get_sale_by_id(self, bike_id):

        db = Database()

        sale = db.fetch_one(
            """
            SELECT
                *,

                (
                    COALESCE(
                        sold_price,
                        0
                    )
                    -
                    COALESCE(
                        purchase_price,
                        0
                    )
                ) AS gross_profit,

                (
                    COALESCE(
                        sold_price,
                        0
                    )
                    -
                    COALESCE(
                        purchase_price,
                        0
                    )
                    -
                    COALESCE(
                        additional_expenses,
                        0
                    )
                ) AS net_profit

            FROM bikes

            WHERE id = %s
            AND status = 'sold'
            """,
            (bike_id,)
        )

        db.close()

        return sale

    # =========================================================
    # MONTHLY PROFIT SUMMARY
    # =========================================================
    def get_monthly_profit(
        self,
        year,
        month
    ):

        db = Database()

        result = db.fetch_one(
            """
            SELECT

                COUNT(*) AS bikes_sold,

                COALESCE(
                    SUM(
                        purchase_price
                    ),
                    0
                ) AS total_purchase_cost,

                COALESCE(
                    SUM(
                        sold_price
                    ),
                    0
                ) AS total_sales,

                COALESCE(
                    SUM(
                        additional_expenses
                    ),
                    0
                ) AS total_expenses,

                COALESCE(
                    SUM(
                        sold_price
                        -
                        COALESCE(
                            purchase_price,
                            0
                        )
                    ),
                    0
                ) AS gross_profit,

                COALESCE(
                    SUM(
                        sold_price
                        -
                        COALESCE(
                            purchase_price,
                            0
                        )
                        -
                        COALESCE(
                            additional_expenses,
                            0
                        )
                    ),
                    0
                ) AS net_profit

            FROM bikes

            WHERE status = 'sold'

            AND sold_price
                IS NOT NULL

            AND sold_date
                IS NOT NULL

            AND YEAR(
                sold_date
            ) = %s

            AND MONTH(
                sold_date
            ) = %s
            """,
            (
                year,
                month
            )
        )

        db.close()

        return result

    # =========================================================
    # YEARLY PROFIT SUMMARY
    # =========================================================
    def get_yearly_profit(self, year):

        db = Database()

        result = db.fetch_one(
            """
            SELECT

                COUNT(*) AS bikes_sold,

                COALESCE(
                    SUM(
                        purchase_price
                    ),
                    0
                ) AS total_purchase_cost,

                COALESCE(
                    SUM(
                        sold_price
                    ),
                    0
                ) AS total_sales,

                COALESCE(
                    SUM(
                        additional_expenses
                    ),
                    0
                ) AS total_expenses,

                COALESCE(
                    SUM(
                        sold_price
                        -
                        COALESCE(
                            purchase_price,
                            0
                        )
                        -
                        COALESCE(
                            additional_expenses,
                            0
                        )
                    ),
                    0
                ) AS net_profit

            FROM bikes

            WHERE status = 'sold'

            AND sold_date
                IS NOT NULL

            AND YEAR(
                sold_date
            ) = %s
            """,
            (year,)
        )

        db.close()

        return result

    # =========================================================
    # MONTH-BY-MONTH PROFIT FOR DASHBOARD
    # =========================================================
    def get_year_monthly_report(self, year):

        db = Database()

        rows = db.fetch_all(
            """
            SELECT

                MONTH(sold_date)
                    AS month,

                COUNT(*)
                    AS bikes_sold,

                COALESCE(
                    SUM(
                        sold_price
                    ),
                    0
                ) AS total_sales,

                COALESCE(
                    SUM(
                        additional_expenses
                    ),
                    0
                ) AS total_expenses,

                COALESCE(
                    SUM(
                        sold_price
                        -
                        COALESCE(
                            purchase_price,
                            0
                        )
                        -
                        COALESCE(
                            additional_expenses,
                            0
                        )
                    ),
                    0
                ) AS net_profit

            FROM bikes

            WHERE status = 'sold'

            AND sold_date
                IS NOT NULL

            AND YEAR(
                sold_date
            ) = %s

            GROUP BY
                MONTH(
                    sold_date
                )

            ORDER BY
                MONTH(
                    sold_date
                )
            """,
            (year,)
        )

        db.close()

        return rows