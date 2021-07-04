import logging
from logging.handlers import RotatingFileHandler

def set_log(filepath, log_name=__name__):
    """
    CRITICAL
    ERROR
    WARNING
    INFO
    DEBUG

    setLevelでDEBUGを指定すると上全てを表示する。
    """

    # create logger
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)


    # create console handler and set level to debug
    s = logging.StreamHandler()
    s.setLevel(logging.INFO)
    r = RotatingFileHandler(filepath, maxBytes=1000000, backupCount=0)
    r.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)d: %(levelname)s - %(message)s','%Y/%m/%d %H:%M:%S')

    # add formatter to ch
    s.setFormatter(formatter)
    r.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(s)
    logger.addHandler(r)

    return logger

log = set_log("/Users/hibiki/Desktop/go/go-react/log/all.log")

if __name__ == '__main__':
    pass