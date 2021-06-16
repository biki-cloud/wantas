from abc import ABCMeta, abstractmethod
import sys
sys.path.append("/Users/hibiki/Desktop/go/go-react")


class AbsStore(metaclass=ABCMeta):
    def __init__(self):
        pass

    # TODO: f邪of時お味
    # FIXME: jファおjフィアお
    @abstractmethod
    def get_all_product(self) -> (list):
        """
        リストの中は辞書で返すが何のキーを持っていた方がいいか定義した方がいいと思う。
        それかクラスで返した方がいいと思う。
        vscodeでtodoができないのか
        """
        pass
