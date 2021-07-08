from abc import ABCMeta, abstractmethod
import sys
sys.path.append("/Users/hibiki/Desktop/go/wants")
sys.path.append("/code")


class AbsStore(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def get_all_product(self) -> (list):
        pass
