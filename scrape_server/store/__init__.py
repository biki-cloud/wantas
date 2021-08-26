import sys
from abc import ABCMeta
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))
sys.path.append(str(Path(__file__).parent.parent.resolve()))
sys.path.append(str(Path(__file__).parent.parent.parent.resolve()))


class AbsStore(metaclass=ABCMeta):
    def __init__(self):
        pass
