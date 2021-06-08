import json
import random
import subprocess
import time
from urllib.request import urlopen

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
        return pre + after
    else:
        return joined.replace("//", "/")

def get_html(url):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    return html

def html_to_soup(html: str):
    return BeautifulSoup(html, "html.parser")

def get_soup(url: str):
    html = get_html(url)
    return html_to_soup(html)


if __name__ == '__main__':
    pass
