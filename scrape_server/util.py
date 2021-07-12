import json
import random
import subprocess
import time
from urllib.request import urlopen
import urllib.robotparser

from bs4 import BeautifulSoup

def dict_to_json(d):
    return json.dumps(d, ensure_ascii=False, indent=4)

def write_json_file(file_path, dic):
    with open(file_path, 'w') as fp:
        json.dump(dic, fp, indent=4, ensure_ascii=False)

def read_json_file(file_path) -> (dict):
    with open(file_path, 'r') as fp:
        return json.load(fp)

def solve_certificate_problem():
    import certifi
    print(f"export SSL_CERT_FILE={certifi.where()}")
    path = certifi.where()
    cmd = f"export SSL_CERT_FILE={certifi.where()}"
    subprocess.call(cmd, shell=True)
    time.sleep(1)

def join_slash(*args):
    joined = ""
    if "https://" not in args[0]:
        joined = "/"
    for a in args:
        joined += a + "/"
    if "https://" in joined or "http://" in joined:
        pre = joined[0:9]
        after = joined[9:].replace("//", "/")
        return_url = pre + after
        # return pre + after
    else:
        return_url = joined.replace("//", "/")
        # return joined.replace("//", "/")
    if return_url[-1] == "/":
        return return_url[:-1]
    return return_url

def get_html(url):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    return html

def html_to_soup(html: str):
    return BeautifulSoup(html, "html.parser")


class UrlCannotFetchError(Exception):
    pass

def get_soup_wrapper(base_url: str):
    """スクレイピングするためにrobots.txtを確認する。
    urlのページ全体をBeautifulSoupに入れ返す関数を返す。
    スクレイピングする時は必ずこの関数を用いる。`

    Args:
        base_url (str): 直下にrobots.txtがあるサイトのベースURL

    Returns:
        get_soup (function): urlページ全体をBeautifulSoupインスタンスにして返す関数を返す。
    """
    rp = urllib.robotparser.RobotFileParser()
    robots_url = join_slash(base_url, "robots.txt")
    rp.set_url(robots_url)
    rp.read()
    delay = rp.crawl_delay("*")
    interval = 0
    if delay == None:
        interval = 1
    else:
        interval = delay

    def get_soup(url: str):
        if rp.can_fetch("*", url) == False:
            raise UrlCannotFetchError(f"This url: {url} can't fetch.")
        time.sleep(interval)
        html = get_html(url)
        return html_to_soup(html)

    return get_soup

if __name__ == '__main__':
    solve_certificate_problem()
