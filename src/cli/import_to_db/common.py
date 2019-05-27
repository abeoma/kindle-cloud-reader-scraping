import os
from typing import List, Dict, TypeVar, Type, Sequence, Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import create_session

from email_sender import send_email
from lib.helper import make_now, split_every
from models_generated import Product
from scraper.common import convert_to_dict


def init_session():
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASS")
    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    dbname = os.environ.get("DB_NAME")

    engine = create_engine(
        f"mysql://{user}:{password}@{host}:{port}/{dbname}?charset=utf8",
        encoding="utf8",
    )
    return create_session(bind=engine, autocommit=True, autoflush=True)


M = TypeVar("M")


def insert_dicts(dicts: Iterator[Dict[str, str]], Model):
    ses = init_session()
    # ses.execute(sa_text(f"TRUNCATE TABLE {Model.__tablename__}"))
    ses.bulk_save_objects([Model(**row) for row in dicts])


def update_dicts(dicts: Iterator[Dict[str, str]], Model):
    ses = init_session()
    ses.bulk_update_mappings(Model, dicts)


def insert_objects(objects: Iterator[M]):
    ses = init_session()
    ses.bulk_save_objects(objects)


def update_objects(objects: Iterator[M], Model):
    def _update(obj: M):
        if getattr(obj, "updated_at"):
            obj.updated_at = make_now()
        return obj

    objects = map(_update, objects)
    ses = init_session()
    ses.bulk_update_mappings(Model, [convert_to_dict(obj) for obj in objects])


def send_products_by_email(brand: str, messages: List[str]):
    top_message: str = "Price updated products are below."
    records_str: str = "\n".join(messages)
    send_email(
        subject=f"PRICE UPDATED: {brand.upper()}",
        body=f"{top_message}\n\n{records_str}",
    )


def upsert_products(records: Iterator[Product], existed_ids: List[str], brand: str):
    price_updated_messages = []

    def upsert_products_internal(splited_records: List[Product]):
        new_records = []
        existed_records = []
        # c = 0
        for record in splited_records:
            # c += 1
            # print(c)
            if record.id not in existed_ids:
                new_records.append(record)
            else:
                # record.price = 1
                prev_record = fetch_by_id(record.id)
                if record.price != prev_record.price:
                    existed_records.append(record)

                    head = f"{record.code} {record.name}"
                    content = f"{prev_record.price}{prev_record.currency} -> {record.price}{record.currency}"
                    price_updated_messages.append(f"{head}:\n{content}\n")
                # if c > 10:
                #     break

        insert_objects(new_records)
        update_objects(existed_records, Product)

    for piece in split_every(n=100, iterable=records):
        upsert_products_internal(piece)

    send_products_by_email(brand=brand, messages=price_updated_messages)


def select_all(model_class: Type[M]) -> Sequence[M]:
    ses = init_session()
    return ses.query(model_class).all()


def fetch_by_id(id: str) -> Product:
    ses = init_session()
    return ses.query(Product).filter(Product.id == id).first()


def fetch_ids(brand: str) -> List[str]:
    ses = init_session()
    tuples = ses.query(Product.id).filter(Product.brand == brand).all()
    return [t[0] for t in tuples]
