from typing import List
import json
import os

from scrape_server.util import *
from scrape_server.store import AbsStore


class DbDriver:
    def __init__(self, database_path):
        self.database_path = database_path

    def put(self, data: List[dict]):
        if os.path.exists(self.database_path):
            elements = self.get_all()
        else:
            elements = []
        for d in data:
            if d not in elements:
                elements.append(d)
        write_json_file(self.database_path, elements)

    def search(self, search_name) -> (List[dict]):
        results = []
        for record in self.get_all():
            if search_name in record['name']:
                results.append(record)
        return results

    def scrape_and_put(self, store: AbsStore):
        elements = store.get_all_product()
        self.put(elements)

    def get_all(self) -> (List[dict]):
        return read_json_file(self.database_path)
