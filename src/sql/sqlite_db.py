import sqlite3, json, io, os, sys, collections, time
import numpy as np
import pandas as pd

parent_folder_path = os.path.dirname( os.path.abspath(__file__)).split(r'src')[0]
sys.path.append(parent_folder_path)

from src.sql.sqlite_sccripts import get_all_table_names

def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

sqlite3.register_adapter(np.ndarray, adapt_array)
sqlite3.register_converter("NUMPYARRAY", convert_array)

def adapt_json(data):
    return (json.dumps(data)).encode("utf-8")

def convert_json(blob):
    return json.loads(blob.decode("utf-8"))

sqlite3.register_adapter(dict, adapt_json)
sqlite3.register_adapter(list, adapt_json)
sqlite3.register_adapter(tuple, adapt_json)
sqlite3.register_adapter(collections.OrderedDict, adapt_json)
sqlite3.register_converter('JSON', convert_json)

class SqliteDB():
    def __init__(self,file_path):
        if os.path.exists(file_path):
            self.file_path = file_path
        else:
            print("path does not exists")
        self.shared_data = pd.DataFrame()
        self.schema = {}

    def connect(self):
        db  = sqlite3.connect(self.file_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cur = db.cursor()
        return db,cur

    def get_schema(self):
        db, cur = self.connect()
        table_names = cur.execute(get_all_table_names).fetchall()
        for (table_name,) in table_names:
            result = cur.execute("PRAGMA table_info('%s')" % table_name).fetchall()
            self.schema.update({table_name:[(xs[0],xs[1],xs[2]) for xs in result] })
        return dict(self.schema)
    
    def excecutescript(self,script):
        try:
            if script and type(script)==str:
                db, cur = self.connect()
                data = pd.read_sql_query(script,db)
                self.shared_data = data
            else:
                self.shared_data = pd.DataFrame()
        except:
            self.shared_data = pd.DataFrame()
        finally:
            return self.shared_data




if __name__ == '__main__':
    sqlite_db = SqliteDB('test.sqlite',parent_folder_path)
    schema = sqlite_db.get_schema()
    print(sqlite_db.excecutescript("bku"))
