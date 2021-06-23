import logging

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
    f = logging.FileHandler(filepath)
    f.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)d: %(levelname)s - %(message)s','%Y/%m/%d %H:%M:%S')

    # add formatter to ch
    s.setFormatter(formatter)
    f.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(s)
    logger.addHandler(f)

    return logger

log = set_log("/Users/hibiki/Desktop/go/go-react/log/all.log")

if __name__ == '__main__':
    pass