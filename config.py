import os

from dotenv import load_dotenv


load_dotenv()


# =========================================================
# SECRET KEY
# =========================================================
SECRET_KEY = os.environ.get(
    "SECRET_KEY"
)

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY environment variable is not set."
    )


# =========================================================
# MYSQL CONFIGURATION
# =========================================================
MYSQL_HOST = os.environ.get(
    "MYSQL_HOST",
    "localhost"
)

MYSQL_USER = os.environ.get(
    "MYSQL_USER",
    "root"
)

MYSQL_PASSWORD = os.environ.get(
    "MYSQL_PASSWORD"
)

if not MYSQL_PASSWORD:
    raise RuntimeError(
        "MYSQL_PASSWORD environment variable is not set."
    )

MYSQL_DATABASE = os.environ.get(
    "MYSQL_DATABASE",
    "supa_auto_link"
)


# =========================================================
# FILE UPLOAD LIMIT
# =========================================================
# 16 MB maximum request size
MAX_CONTENT_LENGTH = (
    16 * 1024 * 1024
)


# =========================================================
# IMAGE EXTENSIONS
# =========================================================
ALLOWED_IMAGE_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


# =========================================================
# SESSION COOKIE SECURITY
# =========================================================
SESSION_COOKIE_SECURE = (
    os.environ
    .get(
        "SESSION_COOKIE_SECURE",
        "false"
    )
    .lower()
    == "true"
)