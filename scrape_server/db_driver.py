from typing import List
import json

from scrape_server.util import *
from scrape_server.store import Store


class DbDriver:
    def __init__(self, database_path):
        self.database_path = database_path

    def put(self, data: List[dict]):
        elements = self.get_all()
        for d in data:
            if d not in elements:
                elements.append(d)
        write_json_file(elements)

    def search(self, search_name) -> (List[dict]):
        result = []
        for record in self.get_all():
            if search_name in record['name']:
                result.append(record)
        return result

    def scrape_and_put(self, store: Store):
        elements = store.get_all_product()
        self.put(elements)


    def get_all(self) -> (List[dict]):
        return read_json_file(self.database_path)
