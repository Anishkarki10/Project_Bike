import pymysql
import config


class Database:
    def __init__(self):
        self.__connection = pymysql.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DATABASE,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
        )

    def fetch_one(self, query, params=None):
        with self.__connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def fetch_all(self, query, params=None):
        with self.__connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute(self, query, params=None):
        with self.__connection.cursor() as cursor:
            cursor.execute(query, params)
            self.__connection.commit()
            return cursor.lastrowid

    def close(self):
        self.__connection.close()

    @staticmethod
    def ensure_database():
        connection = pymysql.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            cursorclass=pymysql.cursors.DictCursor,
        )
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{config.MYSQL_DATABASE}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        connection.commit()
        connection.close()

    @staticmethod
    def create_tables():
        db = Database()

        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'admin',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        ''')

        db.execute('''
            CREATE TABLE IF NOT EXISTS bikes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(180) NOT NULL,
                brand VARCHAR(100) NOT NULL,
                model VARCHAR(120) NOT NULL,
                category VARCHAR(30) NOT NULL,
                year INT NOT NULL,
                engine_cc INT NOT NULL,
                km_travelled INT NOT NULL DEFAULT 0,
                original_price DECIMAL(12,2),
                original_price DECIMAL(12,2) NULL,
                fuel_type VARCHAR(50) DEFAULT 'Petrol',
                transmission VARCHAR(80),
                colour VARCHAR(80),
                condition_text VARCHAR(80),
                owners INT DEFAULT 1,
                reg_number VARCHAR(80),
                short_description VARCHAR(500),
                full_description TEXT,
                features TEXT,
                known_issues TEXT,
                service_info TEXT,
                doc_info TEXT,
                status VARCHAR(30) NOT NULL DEFAULT 'available',
                cover_image VARCHAR(500),
                date_added DATE NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        ''')

        db.execute('''
            CREATE TABLE IF NOT EXISTS bike_images (
                id INT AUTO_INCREMENT PRIMARY KEY,
                bike_id INT NOT NULL,
                image_path VARCHAR(500) NOT NULL,
                sort_order INT DEFAULT 0,
                FOREIGN KEY (bike_id) REFERENCES bikes(id) ON DELETE CASCADE
            ) ENGINE=InnoDB
        ''')

        db.execute('''
            CREATE TABLE IF NOT EXISTS inquiries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(120) NOT NULL,
                phone VARCHAR(40) NOT NULL,
                email VARCHAR(150),
                bike_id INT NULL,
                bike_interested VARCHAR(180),
                message TEXT NOT NULL,
                status VARCHAR(30) DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (bike_id) REFERENCES bikes(id) ON DELETE SET NULL
            ) ENGINE=InnoDB
        ''')

        db.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INT PRIMARY KEY DEFAULT 1,
                business_name VARCHAR(120) DEFAULT 'Supa Auto Link',
                phone VARCHAR(40) DEFAULT '9860541990',
                email VARCHAR(150),
                address VARCHAR(255) DEFAULT 'Nayabazar-16, Kathmandu, Nepal',
                opening_hours TEXT,
                tiktok VARCHAR(255),
                facebook VARCHAR(255),
                instagram VARCHAR(255),
                about_content TEXT,
                logo VARCHAR(255) DEFAULT 'images/logo.png'
            ) ENGINE=InnoDB
        ''')

        if not db.fetch_one('SELECT id FROM settings WHERE id = 1'):
            db.execute('''
                INSERT INTO settings (id, business_name, phone, address, about_content)
                VALUES (1, %s, %s, %s, %s)
            ''', (
                'Supa Auto Link', '9860541990', 'Nayabazar-16, Kathmandu, Nepal',
                'Established in 2023, Supa Auto Link is a second-hand motorcycle and scooter showroom in Nayabazar, Kathmandu. We help customers buy, sell and exchange pre-owned two-wheelers with clear vehicle information and transparent pricing.'
            ))

        # Seed a first admin account for local development.
        if not db.fetch_one("SELECT id FROM users WHERE role='admin' LIMIT 1"):
            from werkzeug.security import generate_password_hash
            db.execute('''
                INSERT INTO users (name, email, password, role)
                VALUES (%s, %s, %s, 'admin')
            ''', ('Administrator', 'admin@supautolink.com', generate_password_hash('admin123')))

        db.close()
