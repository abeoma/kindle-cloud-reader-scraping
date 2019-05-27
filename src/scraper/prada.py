import csv
import json
import re
from pathlib import Path
from typing import Iterator, Dict, Any, List

from bs4 import BeautifulSoup

from crawler.common import ProductPage, cache_filepath, create_id
from lib.constans import Brand
from lib.helper import parse_cache_html, remove_accent
from lib.logger import logger
from repository import BrandRoot
from models_generated import Product

prada_root = BrandRoot(brand_name=Brand.PRADA)
PARSE_FAILED_HTMLS: Path = prada_root.latest_origin_dir() / "parse_failed_htmls.csv"

imgsrc_pattern = re.compile(r"^.+?(https.+jpeg).+?$")
marketer_code_pattern = re.compile(r"^([^_]+)_([^_]+)_.+$")
TARGET_PRODUCT_URL_PATTERN = re.compile(
    r"^https://www\.prada\.com/it/it/(.+)?/?products\.(.+)\.([A-Z\d_]+)\.html$"
)
category_pattern = re.compile(r"^[a-z_/\-]+$")
name_in_url_pattern = re.compile(r"^[A-Za-z\d\-_%,]+$")


def add_cols_picking_from_url(p: Product, url: str) -> Product:
    p.id = create_id(url)
    p.url = url
    mat = TARGET_PRODUCT_URL_PATTERN.match(url)
    p.category = mat.group(1) if mat.group(1) else None
    name_in_url = mat.group(2)
    p.code = mat.group(3)
    if p.category:
        assert category_pattern.match(p.category)
    assert name_in_url_pattern.match(name_in_url)
    assert len(p.code) >= 10
    return p


def price_unit_str(p: Product) -> str:
    # TODO: EUR以外の略記を確認
    unit = "E" if p.currency == "EUR" else None
    assert unit
    return p.price + unit


def pick_images(soup: BeautifulSoup, product: Product) -> Iterator[Dict[str, str]]:
    links: List[str] = []

    def pick_biggest_imgsrc(node: BeautifulSoup) -> str:
        for src_str in node["srcset"].split(","):
            if src_str.endswith("2560w"):
                for text in re.split("\s", src_str):
                    if text.startswith("https") and text.endswith("jpeg"):
                        return text

    def append_link(node: BeautifulSoup) -> List:
        imgsrc = pick_biggest_imgsrc(node)
        if imgsrc not in links:
            links.append(imgsrc)

    main_img = soup.find("div", class_="product-detail-images").find("img")
    append_link(main_img)

    gallery_images = soup.find("div", class_="gallery-container").find_all("img")
    for img in gallery_images:
        append_link(img)

    for i, l in enumerate(links):
        yield dict(
            filename="_".join(
                [product.code, str(i + 1).zfill(2), price_unit_str(product)]
            )
            + Path(l).suffix,
            src=l,
        )


def make_img_editor_record(self):
    if self.is_found:
        return dict(code="_".join([self.code, self.price_unit_str()]), url=self.url)
    else:
        return dict(code="", url="")


def make_marketer_record(self):
    if self.is_found:
        mat = marketer_code_pattern.match(self.code)
        assert mat
        code = " ".join(mat.groups())
        return dict(code=code, price=self.price)
    else:
        return dict(code="", price="")


def convert_to_dict(self) -> Dict[str, Any]:
    d = {}
    for key, value in self.__dict__.items():
        if key == "imgsrcs":
            for index, img in enumerate(value):
                for inner_key, inner_value in img.items():
                    d["image" + str(index + 1) + "_" + inner_key] = inner_value
        elif key not in ["name_in_url", "cache_filename"]:
            d[key] = value
        else:
            pass

    img_editor_record = self.make_img_editor_record()
    for k, v in img_editor_record.items():
        d["img_editor_" + k] = v

    marketer_record = self.make_marketer_record()
    for k, v in marketer_record.items():
        d["marketer_" + k] = v

    return d


def log_parse_failed_html(product: Product):
    exist = PARSE_FAILED_HTMLS.exists()
    fieldnames = [k for k in product.__dict__.keys()]
    row = {k: v for k, v in product.__dict__.items()}

    with PARSE_FAILED_HTMLS.open(mode="a" if exist else "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not exist:
            writer.writeheader()

        writer.writerow(row)


def add_cols_picking_from_cache_file(p: Product) -> Product:
    try:
        cache_file = cache_filepath(
            root=prada_root.latest_product_caches_dir(), url=p.url
        )
        p.cache_file_path = cache_file.resolve()
        p.is_found = True
        soup: BeautifulSoup = parse_cache_html(cache_file)
        if soup.text.startswith("File not found") or (
            soup.title.text == "" and soup.find("h1").text == "404"
        ):
            p.is_found = False
            return p

        page_title, code = soup.title.text.split(" | Prada - ")
        assert page_title
        assert code == p.code
        assert len(page_title) > 0
        p.name = remove_accent(page_title).upper()

        price_info = soup.find("div", class_="price")
        price = re.sub(r"[\s.]", "", price_info.contents[2])
        assert re.match(r"^[\d]+$", price)
        p.price = price

        currency = price_info.abbr["title"]
        assert re.match(r"^[A-Z]{3}$", currency)
        p.currency = currency

        p.image_dirname = "_".join([p.code, p.name, price_unit_str(p)])

        image_dicts: Iterator[Dict[str, str]] = pick_images(soup, product=p)
        p.images_json = json.dumps([d for d in image_dicts])

        return p

    except AssertionError as e:
        log_parse_failed_html(p)
        logger.error(e)

    except Exception as e:
        log_parse_failed_html(p)
        logger.error(e)


def scrape_prada(page: ProductPage) -> Product:
    product = Product()
    product.brand = "prada"
    product = add_cols_picking_from_url(product, url=page.url)
    product = add_cols_picking_from_cache_file(product)
    return product
