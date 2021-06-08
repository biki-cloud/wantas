from abc import abstractmethod

class Store(object):
    def __init__(self):
        pass

    @abstractmethod
    def get_all_product(self):
        pass
