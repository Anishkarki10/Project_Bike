from app.models.base_model import BaseModel
from app.models.database import Database


class Bike(BaseModel):
    @property
    def table(self):
        return 'bikes'

    def get_all(self, status=None, brand=None, category=None, min_price=None, max_price=None, search=None):
        sql = 'SELECT * FROM bikes WHERE 1=1'
        params = []
        if status:
            sql += ' AND status=%s'; params.append(status)
        if brand:
            sql += ' AND brand=%s'; params.append(brand)
        if category:
            sql += ' AND category=%s'; params.append(category)
        if min_price:
            sql += ' AND price >= %s'; params.append(min_price)
        if max_price:
            sql += ' AND price <= %s'; params.append(max_price)
        if search:
            sql += ' AND (name LIKE %s OR brand LIKE %s OR model LIKE %s)'
            term = f'%{search}%'; params.extend([term, term, term])
        sql += ' ORDER BY id DESC'
        db = Database(); rows = db.fetch_all(sql, tuple(params)); db.close()
        return rows

    def get_available_featured(self, limit=6):
        db = Database()
        rows = db.fetch_all('SELECT * FROM bikes WHERE status="available" ORDER BY id DESC LIMIT %s', (limit,))
        db.close(); return rows

    def get_brands(self):
        db = Database(); rows = db.fetch_all('SELECT DISTINCT brand FROM bikes ORDER BY brand'); db.close()
        return [r['brand'] for r in rows]

    def get_images(self, bike_id):
        db = Database(); rows = db.fetch_all('SELECT * FROM bike_images WHERE bike_id=%s ORDER BY sort_order, id', (bike_id,)); db.close()
        return [r['image_path'] for r in rows]

    def save(self, data):
        db = Database()
        bike_id = db.execute('''
            INSERT INTO bikes
            (name, brand, model, category, year, engine_cc, km_travelled, price, original_price,
             fuel_type, transmission, colour, condition_text, owners, reg_number, short_description,
             full_description, features, known_issues, service_info, doc_info, status, cover_image)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''', (
            data['name'], data['brand'], data['model'], data['category'], data['year'], data['engine_cc'],
            data['km_travelled'], data['price'], data.get('original_price'), data.get('fuel_type'),
            data.get('transmission'), data.get('colour'), data.get('condition_text'), data.get('owners', 1),
            data.get('reg_number'), data.get('short_description'), data.get('full_description'),
            data.get('features'), data.get('known_issues'), data.get('service_info'), data.get('doc_info'),
            data.get('status', 'available'), data.get('cover_image')
        ))
        db.close(); return bike_id

    def update(self, bike_id, data):
        db = Database()
        db.execute('''
            UPDATE bikes SET name=%s, brand=%s, model=%s, category=%s, year=%s, engine_cc=%s,
            km_travelled=%s, price=%s, original_price=%s, fuel_type=%s, transmission=%s, colour=%s,
            condition_text=%s, owners=%s, reg_number=%s, short_description=%s, full_description=%s,
            features=%s, known_issues=%s, service_info=%s, doc_info=%s, status=%s, cover_image=%s
            WHERE id=%s
        ''', (
            data['name'], data['brand'], data['model'], data['category'], data['year'], data['engine_cc'],
            data['km_travelled'], data['price'], data.get('original_price'), data.get('fuel_type'),
            data.get('transmission'), data.get('colour'), data.get('condition_text'), data.get('owners', 1),
            data.get('reg_number'), data.get('short_description'), data.get('full_description'),
            data.get('features'), data.get('known_issues'), data.get('service_info'), data.get('doc_info'),
            data.get('status', 'available'), data.get('cover_image'), bike_id
        ))
        db.close()

    def add_image(self, bike_id, image_path, sort_order=0):
        db=Database(); db.execute('INSERT INTO bike_images (bike_id,image_path,sort_order) VALUES (%s,%s,%s)', (bike_id,image_path,sort_order)); db.close()

    def clear_images(self, bike_id):
        db=Database(); db.execute('DELETE FROM bike_images WHERE bike_id=%s', (bike_id,)); db.close()

    def toggle_status(self, bike_id):
        db=Database(); db.execute("UPDATE bikes SET status = CASE WHEN status='available' THEN 'sold' ELSE 'available' END WHERE id=%s", (bike_id,)); db.close()

    def counts(self):
        db=Database()
        total=db.fetch_one('SELECT COUNT(*) total FROM bikes')['total']
        available=db.fetch_one("SELECT COUNT(*) total FROM bikes WHERE status='available'")['total']
        sold=db.fetch_one("SELECT COUNT(*) total FROM bikes WHERE status='sold'")['total']
        db.close(); return {'total':total,'available':available,'sold':sold}
