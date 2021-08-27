import json
import time
import urllib.robotparser
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
    time.sleep(1)


def url_join(*args):
    joined_str = ""
    for i in range(len(args)):
        if "http://" in args[i] or "https://" in args[i]:
            joined_str += args[i] + "/"
        else:
            if i == len(args) - 1:
                joined_str += args[i][0].replace("/", "") + args[i][1:-1] + args[i][-1].replace("/", "")
            else:
                joined_str += args[i].replace("/", "") + "/"
    return joined_str


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
    robots_url = url_join(base_url, "robots.txt")
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
        max_continue_count = 10
        continue_count = 0
        while True:
            time.sleep(interval)
            try:
                html = get_html(url)
                break
            except urllib.error.HTTPError:
                continue_count += 1
                if continue_count > max_continue_count:
                    break
                continue
        return html_to_soup(html)

    return get_soup


if __name__ == '__main__':
    solve_certificate_problem()
