from typing import List
import json


def dict_to_json(d) -> str:
    return json.dumps(d, ensure_ascii=False, indent=4)

def write_json_file(file_path, dic):
    with open(file_path, 'w') as fp:
        json.dump(dic, fp, indent=4, ensure_ascii=False)

def read_json_file(file_path) -> dict:
    with open(file_path, 'r') as fp:
        return json.load(fp)


class Database:
    def __init__(self, database_path):
        self.database_path = database_path
        self.database = []

    def register(self, li: List[dict]):
        pass

    def search(self, search_name) -> List[dict]:
        pass

    def get_all(self) -> List[dict]:
        pass
