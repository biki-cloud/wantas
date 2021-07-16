import pytest
from typing import List
import grpc
import sys
import os
import logging as log
import dataset
sys.path.append("/Users/hibiki/Desktop/go/wantas")
sys.path.append("/code")
from scrape_server import server


def test_server():
    results = server.search("パスタ", 35.858968399999995, 139.4988529)
    assert 20 == len(results)
    for ele in results:
        if ele['store_table_name'] == "store_seveneleven":
            assert "セブンイレブンふじみ野亀久保店" == ele['store_name']
        if ele['store_table_name'] == "store_familymart":
            assert "ファミリーマートふじみ野亀久保店" == ele['store_name']
        if ele['store_table_name'] == "store_lawson":
            assert "ローソン大井武蔵野店" == ele['store_name']