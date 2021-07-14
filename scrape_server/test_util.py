import pytest

from scrape_server import util

def test_join_slash():
    assert "https://www.lawson.co.jp/aa/bb/cc" == util.url_join("https://www.lawson.co.jp", "aa", "bb", "cc/")
    assert "http://www.lawson.co.jp/aa/bb/cc" == util.url_join("http://www.lawson.co.jp", "aa", "bb", "cc/")
    assert "http://www.lawson.co.jp/aa/bb/cc" == util.url_join("http://www.lawson.co.jp", "aa/", "/bb", "cc/")
    assert "https://www.family.co.jp/content/dam/family/goods/0750684.jpg" == util.url_join("https://www.family.co.jp", "/content/dam/family/goods/0750684.jpg")