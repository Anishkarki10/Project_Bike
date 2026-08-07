from app.models.base_model import BaseModel
from app.models.database import Database


class Inquiry(BaseModel):
    @property
    def table(self):
        return 'inquiries'

    def create(self, data):
        db=Database()
        db.execute('''INSERT INTO inquiries (name,phone,email,bike_id,bike_interested,message,status)
                      VALUES (%s,%s,%s,%s,%s,%s,'new')''',
                   (data['name'],data['phone'],data.get('email'),data.get('bike_id'),data.get('bike_interested'),data['message']))
        db.close()

    def get_all_with_bike(self):
        db=Database(); rows=db.fetch_all('''SELECT inquiries.*, bikes.name bike_name FROM inquiries
            LEFT JOIN bikes ON inquiries.bike_id=bikes.id ORDER BY inquiries.id DESC'''); db.close(); return rows

    def update_status(self, inquiry_id, status):
        db=Database(); db.execute('UPDATE inquiries SET status=%s WHERE id=%s',(status,inquiry_id)); db.close()

    def count_new(self):
        db=Database(); n=db.fetch_one("SELECT COUNT(*) total FROM inquiries WHERE status='new'")['total']; db.close(); return n
