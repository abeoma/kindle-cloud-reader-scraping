import re
from _md5 import md5
from pathlib import Path
from typing import Dict, Iterator, List, Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from lib.helper import read_html, parse_html


def create_id(text: str) -> str:
    return md5(text.encode()).hexdigest()


def cache_filename(url: str) -> str:
    return create_id(url)


def cache_filepath(root: Path, url: str) -> Path:
    return root / cache_filename(url)


class ProductPage(object):
    def __init__(self, url: str, lastmod: str = None):
        self.url: str = url
        self.lastmod: str = lastmod


def pick_sitename(url: str) -> str:
    domain = urlparse(url).netloc
    return re.sub(r"(^www\.|\.co\.jp/?$|\.com/?$|.ocnk.net/?$)", "", domain)


def pick_urls_from_sitemap(sitemap: str) -> Iterator[Dict[str, Optional[str]]]:
    sitemap: BeautifulSoup = parse_html(sitemap)
    records: List[BeautifulSoup] = [url for url in sitemap.find_all("url")]
    records: Iterator[Dict[str, BeautifulSoup]] = map(
        lambda r: dict(url=r.find("loc"), lastmod=r.find("lastmod")), records
    )
    records = filter(lambda r: r["url"] is not None, records)
    for record in records:
        lastmod = record["lastmod"]
        record["url"] = record["url"].text
        record["lastmod"] = lastmod.text if lastmod is not None else None
        yield record


def pick_urls_from_sitemap_url(
    url: str, is_root: bool = True
) -> Iterator[Dict[str, Optional[str]]]:
    sitemap: str = read_html(url + "/sitemap.xml") if is_root else read_html(url)
    yield pick_urls_from_sitemap(sitemap)


def cache_page(url: str, output_file: Path):
    html: str = read_html(url)
    with output_file.open("w") as f:
        f.write(html)
