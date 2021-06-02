import json
import random
from urllib.request import urlopen
from bs4 import BeautifulSoup

def dict_to_json(d):
    return json.dumps(d, ensure_ascii=False, indent=4)

def solve_certificate_problem():
    import certifi
    print(f"export SSL_CERT_FILE={certifi.where()}")

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

def get_products_tag(url) -> list:
    soup = get_soup(url)
    return soup.findAll("div", {"class": "list_inner"})

