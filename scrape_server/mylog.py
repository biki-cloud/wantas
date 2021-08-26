import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


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
    formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)d: %(levelname)s - %(message)s',
                                  '%Y/%m/%d %H:%M:%S')

    # add formatter to ch
    s.setFormatter(formatter)
    r.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(s)
    logger.addHandler(r)

    return logger


# if socket.gethostname() == "hibikinoiMac.local":
#     log = set_log(f"{str(Path(__file__).parent.parent.resolve())}/log/all.log")
# elif socket.gethostname() == "ip-10-0-0-234.us-east-2.compute.internal":
#     log = set_log("/home/hibiki/wantas/log/all.log")
# else:
#     log = set_log("/log/all.log")

log = set_log(f"{str(Path(__file__).parent.parent.resolve())}/log/all.log")

if __name__ == '__main__':
    pass
