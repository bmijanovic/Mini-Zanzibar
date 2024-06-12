import os

import plyvel


class LevelDBHandler:
    def __init__(self, db_path='leveldb'):
        #  print me current directory
        print("current directory is: ", os.getcwd())
        self.db = plyvel.DB(db_path, create_if_missing=True)

    def put_acl(self, key, value):
        self.db.put(key.encode('utf-8'), value.encode('utf-8'))

    def get_acl(self, key):
        value = self.db.get(key.encode('utf-8'))
        return value.decode('utf-8') if value else None

    def delete_acl(self, key):
        self.db.delete(key.encode('utf-8'))

    def close(self):
        self.db.close()
