import os, sys, json, logging, logging.config, time, errno, sqlite3

from datetime import datetime
from logging import FileHandler
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from threading import Thread
from queue import Queue
from collections import deque

parent_folder_path = os.path.dirname( os.path.abspath(__file__)).split(r'src')[0]
sys.path.append(parent_folder_path)

logging_config_path = parent_folder_path+ "/src/common/logger_config.json"

from src.common.tools import mkdir_p


class AsyncHandlerMixin(object):
    def __init__(self, *args, **kwargs):
        super(AsyncHandlerMixin, self).__init__(*args, **kwargs)
        self.__queue = Queue()
        self.__thread = Thread(target=self.__loop)
        self.__thread.daemon = True
        self.__thread.start()

    def emit(self, record):
        self.__queue.put(record)

    def __loop(self):
        while True:
            record = self.__queue.get()
            try:
                super(AsyncHandlerMixin, self).emit(record)
            except:
                pass


class AsyncRotatingFileHandler(AsyncHandlerMixin, RotatingFileHandler):
    pass




def getLogger( logger_name,logfile = "common.log", path=None, maxBytes=2e+7):
    logger = logging.getLogger(logger_name)
    default_level=logging.INFO

    if os.path.exists(logging_config_path):
        with open(logging_config_path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
    if not path:
        path = parent_folder_path+"/logs/"
    mkdir_p(path)
    
    logfilepath = os.path.join(path, logfile)

    handler = AsyncRotatingFileHandler(logfilepath, maxBytes=2e+7, backupCount=20)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger



def test_logger( ):
    logger = getLogger("data.log","my_logger3")
    while True:
        try:
            logger.info("info!!")
            logger.debug("debug!")
            logger.error("error!")
            time.sleep(0.005)
        except KeyboardInterrupt:
            logger.error("exception")
            logger.exception("message:")
            break
        except:
            raise

if __name__ == '__main__':
    test_logger()


    

