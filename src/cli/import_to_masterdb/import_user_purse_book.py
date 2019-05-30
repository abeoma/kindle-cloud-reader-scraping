from typing import Dict, Iterator, Any

from cli.import_to_masterdb.common import upsert_book_dicts
from lib.helper import new_pk
from models.master_models_generated import User
from services.crawler import crawl
from services.scraper import scrape


def import_user_purse_books(user: User):
    crawl(user=user)
    output_records: Iterator[Dict[str, Any]] = scrape(user=user)
    output_records = map(
        lambda r: dict(r, id=new_pk(), user_id=user.id), output_records
    )
    upsert_book_dicts(output_records)
