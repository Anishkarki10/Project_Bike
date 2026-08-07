from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base_model import BaseModel
from app.models.database import Database


class User(BaseModel):
    @property
    def table(self):
        return 'users'

    def find_by_email(self, email):
        db = Database()
        row = db.fetch_one('SELECT * FROM users WHERE email = %s', (email,))
        db.close()
        return row

    def check_password(self, hashed_password, plain_password):
        return check_password_hash(hashed_password, plain_password)

    def update_password(self, user_id, plain_password):
        db = Database()
        db.execute('UPDATE users SET password=%s WHERE id=%s', (generate_password_hash(plain_password), user_id))
        db.close()
