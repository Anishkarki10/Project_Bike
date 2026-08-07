import os

SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-secret-key')
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'REDACTED')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'supa_auto_link')

MAX_CONTENT_LENGTH = 16 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
