from abc import ABC, abstractmethod
from app.models.database import Database


class BaseModel(ABC):
    @property
    @abstractmethod
    def table(self):
        pass

    def find_by_id(self, record_id):
        db = Database()
        result = db.fetch_one(f'SELECT * FROM {self.table} WHERE id = %s', (record_id,))
        db.close()
        return result

    def find_all(self, order_by='id DESC'):
        db = Database()
        result = db.fetch_all(f'SELECT * FROM {self.table} ORDER BY {order_by}')
        db.close()
        return result

    def delete_by_id(self, record_id):
        db = Database()
        db.execute(f'DELETE FROM {self.table} WHERE id = %s', (record_id,))
        db.close()
