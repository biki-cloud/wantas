import pytest
import os
import sys
sys.path.append("/Users/hibiki/Desktop/go/wantas")
sys.path.append("/code")

import dataset
import requests
import time

from scrape_server.util import *
from scrape_server.database import db


def test_JsonDbDriver(tmp_path):
    # pytestが自動でディレクトリを作成
    d = tmp_path / "sub"
    d.mkdir()
    database_file_path = d / "db.json"
    db_driver = db.JsonDbDriver(database_file_path)
    li = [
        {
            "name": "biki"
        },
        {
            "age": 22
        }
    ]
    db_driver.put(li)
    assert db_driver.get_all() == li
