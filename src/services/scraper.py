from pathlib import Path
from typing import Iterator, Dict

from bs4 import BeautifulSoup

from lib.helper import find_latest_source_file, parse_cache_html
from models.master_models_generated import User
from services.common import CACHE_ROOT


def pick_books(filepath: Path) -> Iterator[Dict[str, str]]:
    soup: BeautifulSoup = parse_cache_html(filepath)
    book_containers = soup.find_all("div", class_="book_container")
    for i, container in enumerate(book_containers):
        title = container.find("div", class_="book_title")
        author = container.find("div", class_="book_author")
        img = container.find("img")
        imgsrc = (
            img.get("src")
            if img and "img_alt_cover.png" not in img.get("src")
            else None
        )  # 読み込みに失敗するとsrcが'./images/override/library/img_alt_cover.png'となる

        yield dict(
            asin=container.get("id"),
            title=title.text if title else None,
            author=author.text if author else None,
            image_src=imgsrc,
        )


def scrape(user: User):
    cache_filepath: Path = find_latest_source_file(
        parent_dir=CACHE_ROOT / user.id, suffix=".html"
    )
    return pick_books(cache_filepath)
