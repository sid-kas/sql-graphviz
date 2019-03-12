import sqlite3, json, io, os, sys, collections, time
import numpy as np
import pandas as pd


parent_folder_path = os.path.dirname( os.path.abspath(__file__)).split(r'src')[0]
sys.path.append(parent_folder_path)

from src.sql.sqlite_sccripts import get_all_table_names
from src.common.logging_service import getLogger

logger = getLogger("sqlite_db")

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

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
        try:
            if os.path.exists(file_path):
                self.file_path = file_path
                logger.info("db path: "+self.file_path)
            else:
                logger.info("path does not exists")
            self.schema = {}
        except:
            logger.exception("SqliteDb>>init")

    def connect(self):
        db  = sqlite3.connect(self.file_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cur = db.cursor()
        return db,cur

    def get_schema(self):
        _, cur = self.connect()
        table_names = cur.execute(get_all_table_names).fetchall()
        for (table_name,) in table_names:
            result = cur.execute("PRAGMA table_info('%s')" % table_name).fetchall()
            self.schema.update({table_name:[(xs[0],xs[1],xs[2]) for xs in result] })
        return dict(self.schema)
    
    def excecutescript(self,script):
        dict_data = {}
        try:
            if script and type(script)==str:
                _, cur = self.connect()
                data = np.array(cur.execute(script).fetchall())
                dict_data = {description[0]:data[:,i] for i,description in enumerate(cur.description)}
                logger.info("data len: "+str(len(dict_data))+", keys: "+str((dict_data.keys())))
        except:
            logger.exception("from>>excecutescript")
        finally:
            return dict_data

script = """
SELECT motorCurrent, feederCurrent, remotePWM,outputPWM,inputVC,motorControlDesired,depth
FROM SensorData where motorCurrent>0;
"""


if __name__ == '__main__':
    sqlite_db = SqliteDB(parent_folder_path+'SensorData.sqlite')
    schema = sqlite_db.get_schema()
    sqlite_db.excecutescript(script)
