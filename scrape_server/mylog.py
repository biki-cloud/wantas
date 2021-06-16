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
    s.setLevel(logging.DEBUG)
    f = logging.FileHandler(filepath)
    f.setLevel(logging.DEBUG)

    # create formatter
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)d: %(levelname)s - %(message)s','%Y/%m/%d %H:%M:%S')

    # add formatter to ch
    s.setFormatter(formatter)
    f.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(s)
    logger.addHandler(f)

    return logger

if __name__ == '__main__':
    log = set_log("file.log")
    log.debug("hello")