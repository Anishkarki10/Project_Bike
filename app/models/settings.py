from app.models.database import Database


class Settings:
    def get(self):
        db=Database(); row=db.fetch_one('SELECT * FROM settings WHERE id=1'); db.close(); return row

    def update(self, data):
        db=Database(); db.execute('''UPDATE settings SET business_name=%s,phone=%s,email=%s,address=%s,
            opening_hours=%s,tiktok=%s,facebook=%s,instagram=%s,about_content=%s,logo=%s WHERE id=1''',
            (data.get('business_name'),data.get('phone'),data.get('email'),data.get('address'),data.get('opening_hours'),
             data.get('tiktok'),data.get('facebook'),data.get('instagram'),data.get('about_content'),data.get('logo')))
        db.close()
