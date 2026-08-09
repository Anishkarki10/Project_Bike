import os
import pymysql
import config


class Database:

    # =========================================================
    # DATABASE CONNECTION
    # =========================================================
    def __init__(self):

        self.__connection = pymysql.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DATABASE,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )

    # =========================================================
    # FETCH ONE
    # =========================================================
    def fetch_one(
        self,
        query,
        params=None
    ):

        with self.__connection.cursor() as cursor:

            cursor.execute(
                query,
                params
            )

            return cursor.fetchone()

    # =========================================================
    # FETCH ALL
    # =========================================================
    def fetch_all(
        self,
        query,
        params=None
    ):

        with self.__connection.cursor() as cursor:

            cursor.execute(
                query,
                params
            )

            return cursor.fetchall()

    # =========================================================
    # EXECUTE
    # =========================================================
    def execute(
        self,
        query,
        params=None
    ):

        try:

            with self.__connection.cursor() as cursor:

                cursor.execute(
                    query,
                    params
                )

                self.__connection.commit()

                return cursor.lastrowid

        except Exception:

            self.__connection.rollback()

            raise

    # =========================================================
    # CLOSE
    # =========================================================
    def close(self):

        self.__connection.close()

    # =========================================================
    # ENSURE DATABASE
    # =========================================================
    @staticmethod
    def ensure_database():

        connection = pymysql.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            cursorclass=pymysql.cursors.DictCursor
        )

        try:

            with connection.cursor() as cursor:

                cursor.execute(
                    f"""
                    CREATE DATABASE IF NOT EXISTS
                    `{config.MYSQL_DATABASE}`
                    CHARACTER SET utf8mb4
                    COLLATE utf8mb4_unicode_ci
                    """
                )

            connection.commit()

        finally:

            connection.close()

    # =========================================================
    # CHECK COLUMN
    # =========================================================
    @staticmethod
    def column_exists(
        db,
        table_name,
        column_name
    ):

        result = db.fetch_one(
            """
            SELECT COUNT(*) AS total

            FROM information_schema.COLUMNS

            WHERE TABLE_SCHEMA = %s
            AND TABLE_NAME = %s
            AND COLUMN_NAME = %s
            """,
            (
                config.MYSQL_DATABASE,
                table_name,
                column_name
            )
        )

        return (
            result["total"] > 0
        )

    # =========================================================
    # ADD COLUMN SAFELY
    # =========================================================
    @staticmethod
    def add_column_if_missing(
        db,
        table_name,
        column_name,
        column_definition
    ):

        if not Database.column_exists(
            db,
            table_name,
            column_name
        ):

            db.execute(
                f"""
                ALTER TABLE `{table_name}`

                ADD COLUMN `{column_name}`
                {column_definition}
                """
            )

            print(
                f"Added column: "
                f"{table_name}.{column_name}"
            )

    # =========================================================
    # CREATE TABLES
    # =========================================================
    @staticmethod
    def create_tables():

        # THIS is where db becomes available
        db = Database()

        # =====================================================
        # USERS
        # =====================================================
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (

                id INT AUTO_INCREMENT PRIMARY KEY,

                name VARCHAR(100)
                NOT NULL,

                email VARCHAR(150)
                NOT NULL
                UNIQUE,

                password VARCHAR(255)
                NOT NULL,

                role VARCHAR(20)
                NOT NULL
                DEFAULT 'admin',

                created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP

            ) ENGINE=InnoDB
            """
        )

        # =====================================================
        # BIKES
        # =====================================================
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS bikes (

                id INT AUTO_INCREMENT PRIMARY KEY,

                name VARCHAR(180)
                NOT NULL,

                brand VARCHAR(100)
                NOT NULL,

                model VARCHAR(120)
                NOT NULL,

                category VARCHAR(30)
                NOT NULL,

                year INT
                NOT NULL,

                engine_cc INT
                NOT NULL,

                km_travelled INT
                NOT NULL
                DEFAULT 0,

                price DECIMAL(12,2)
                NOT NULL,

                original_price DECIMAL(12,2)
                NULL,

                purchase_price DECIMAL(12,2)
                NULL,

                purchase_date DATE
                NULL,

                sold_price DECIMAL(12,2)
                NULL,

                sold_date DATE
                NULL,

                additional_expenses DECIMAL(12,2)
                NOT NULL
                DEFAULT 0,

                fuel_type VARCHAR(50)
                DEFAULT 'Petrol',

                transmission VARCHAR(80),

                colour VARCHAR(80),

                condition_text VARCHAR(80),

                owners INT
                DEFAULT 1,

                reg_number VARCHAR(80),

                short_description VARCHAR(500),

                full_description TEXT,

                features TEXT,

                known_issues TEXT,

                service_info TEXT,

                doc_info TEXT,

                status VARCHAR(30)
                NOT NULL
                DEFAULT 'available',

                cover_image VARCHAR(500),

                date_added DATE
                NULL,

                created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP

            ) ENGINE=InnoDB
            """
        )

        # =====================================================
        # EXISTING DB MIGRATIONS
        # =====================================================
        Database.add_column_if_missing(
            db,
            "bikes",
            "price",
            "DECIMAL(12,2) NOT NULL DEFAULT 0"
        )

        Database.add_column_if_missing(
            db,
            "bikes",
            "original_price",
            "DECIMAL(12,2) NULL"
        )

        Database.add_column_if_missing(
            db,
            "bikes",
            "purchase_price",
            "DECIMAL(12,2) NULL"
        )

        Database.add_column_if_missing(
            db,
            "bikes",
            "purchase_date",
            "DATE NULL"
        )

        Database.add_column_if_missing(
            db,
            "bikes",
            "sold_price",
            "DECIMAL(12,2) NULL"
        )

        Database.add_column_if_missing(
            db,
            "bikes",
            "sold_date",
            "DATE NULL"
        )

        Database.add_column_if_missing(
            db,
            "bikes",
            "additional_expenses",
            "DECIMAL(12,2) NOT NULL DEFAULT 0"
        )

        Database.add_column_if_missing(
            db,
            "bikes",
            "date_added",
            "DATE NULL"
        )

        # =====================================================
        # CORRECT MONEY TYPES
        # =====================================================
        db.execute(
            """
            ALTER TABLE bikes

            MODIFY COLUMN price
            DECIMAL(12,2)
            NOT NULL
            """
        )

        db.execute(
            """
            ALTER TABLE bikes

            MODIFY COLUMN original_price
            DECIMAL(12,2)
            NULL
            """
        )

        db.execute(
            """
            ALTER TABLE bikes

            MODIFY COLUMN purchase_price
            DECIMAL(12,2)
            NULL
            """
        )

        db.execute(
            """
            ALTER TABLE bikes

            MODIFY COLUMN sold_price
            DECIMAL(12,2)
            NULL
            """
        )

        db.execute(
            """
            ALTER TABLE bikes

            MODIFY COLUMN additional_expenses
            DECIMAL(12,2)
            NOT NULL
            DEFAULT 0
            """
        )

        # =====================================================
        # BIKE IMAGES
        # =====================================================
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS bike_images (

                id INT AUTO_INCREMENT PRIMARY KEY,

                bike_id INT
                NOT NULL,

                image_path VARCHAR(500)
                NOT NULL,

                sort_order INT
                DEFAULT 0,

                FOREIGN KEY (bike_id)
                REFERENCES bikes(id)
                ON DELETE CASCADE

            ) ENGINE=InnoDB
            """
        )

        # =====================================================
        # INQUIRIES
        # =====================================================
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS inquiries (

                id INT AUTO_INCREMENT PRIMARY KEY,

                name VARCHAR(120)
                NOT NULL,

                phone VARCHAR(40)
                NOT NULL,

                email VARCHAR(150),

                bike_id INT
                NULL,

                bike_interested VARCHAR(180),

                message TEXT
                NOT NULL,

                status VARCHAR(30)
                DEFAULT 'new',

                created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (bike_id)
                REFERENCES bikes(id)
                ON DELETE SET NULL

            ) ENGINE=InnoDB
            """
        )

        # =====================================================
        # SETTINGS
        # =====================================================
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (

                id INT PRIMARY KEY
                DEFAULT 1,

                business_name VARCHAR(120)
                DEFAULT 'Supa Auto Link',

                phone VARCHAR(40)
                DEFAULT '9860541990',

                email VARCHAR(150),

                address VARCHAR(255)
                DEFAULT 'Nayabazar-16, Kathmandu, Nepal',

                opening_hours TEXT,

                tiktok VARCHAR(255),

                facebook VARCHAR(255),

                instagram VARCHAR(255),

                about_content TEXT,

                logo VARCHAR(255)
                DEFAULT 'images/logo.png'

            ) ENGINE=InnoDB
            """
        )

        # =====================================================
        # DEFAULT SETTINGS
        # =====================================================
        settings = db.fetch_one(
            """
            SELECT id

            FROM settings

            WHERE id = 1
            """
        )

        if not settings:

            db.execute(
                """
                INSERT INTO settings
                (
                    id,
                    business_name,
                    phone,
                    address,
                    about_content
                )

                VALUES
                (
                    1,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    "Supa Auto Link",

                    "9860541990",

                    "Nayabazar-16, Kathmandu, Nepal",

                    (
                        "Established in 2023, "
                        "Supa Auto Link is a "
                        "second-hand motorcycle "
                        "and scooter showroom in "
                        "Nayabazar, Kathmandu."
                    )
                )
            )

        # =====================================================
        # INITIAL ADMIN
        # =====================================================
        admin = db.fetch_one(
            """
            SELECT id

            FROM users

            WHERE role = 'admin'

            LIMIT 1
            """
        )

        if not admin:

            from werkzeug.security import (
                generate_password_hash
            )

            admin_name = os.environ.get(
                "ADMIN_NAME"
            )

            admin_email = os.environ.get(
                "ADMIN_EMAIL"
            )

            admin_password = os.environ.get(
                "ADMIN_PASSWORD"
            )

            if not all([
                admin_name,
                admin_email,
                admin_password
            ]):

                db.close()

                raise RuntimeError(
                    "No admin account exists and "
                    "ADMIN_NAME, ADMIN_EMAIL and "
                    "ADMIN_PASSWORD are not configured."
                )

            if len(admin_password) < 12:

                db.close()

                raise RuntimeError(
                    "ADMIN_PASSWORD must contain "
                    "at least 12 characters."
                )

            db.execute(
                """
                INSERT INTO users
                (
                    name,
                    email,
                    password,
                    role
                )

                VALUES
                (
                    %s,
                    %s,
                    %s,
                    'admin'
                )
                """,
                (
                    admin_name.strip(),

                    admin_email
                    .strip()
                    .lower(),

                    generate_password_hash(
                        admin_password
                    )
                )
            )

            print(
                "Initial administrator created."
            )

        # =====================================================
        # CLOSE
        # =====================================================
        db.close()

        print(
            "Database tables ready successfully."
        )