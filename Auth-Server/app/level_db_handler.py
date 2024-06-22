import os
import plyvel


class LevelDBHandler:
    def __init__(self, db_path='app/leveldb_data'):
        self.db = plyvel.DB(db_path, create_if_missing=True)

    def put(self, key, value):
        self.db.put(key.encode('utf-8'), value.encode('utf-8'))

    def get(self, key):
        value = self.db.get(key.encode('utf-8'))
        return value.decode('utf-8') if value else None

    def delete(self, key):
        self.db.delete(key.encode('utf-8'))

    def close(self):
        self.db.close()
