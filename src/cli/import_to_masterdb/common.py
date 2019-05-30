import os
from typing import Dict, TypeVar, Type, Sequence, Iterator, Any

from sqlalchemy import create_engine
from sqlalchemy.orm import create_session

from lib.helper import make_now
from models.master_models_generated import UserPurseBook


def init_session():
    user = os.environ.get("MASTER_DB_USER")
    password = os.environ.get("MASTER_DB_PASS")
    host = os.environ.get("MASTER_DB_HOST")
    port = os.environ.get("MASTER_DB_PORT")
    dbname = os.environ.get("MASTER_DB_NAME")

    engine = create_engine(
        f"mysql://{user}:{password}@{host}:{port}/{dbname}?charset=utf8",
        encoding="utf8",
    )
    return create_session(bind=engine, autocommit=True, autoflush=True)


M = TypeVar("M")


def insert_dict(record: Dict[str, Any], Model):
    ses = init_session()
    ses.bulk_save_objects([Model(**record)])


def insert_dicts(dicts: Iterator[Dict[str, Any]], Model):
    ses = init_session()
    # ses.execute(sa_text(f"TRUNCATE TABLE {Model.__tablename__}"))
    ses.bulk_save_objects([Model(**row) for row in dicts])


def update_dicts(dicts: Iterator[Dict[str, Any]], Model):
    ses = init_session()
    ses.bulk_update_mappings(Model, dicts)


def insert_objects(objects: Iterator[M]):
    ses = init_session()
    ses.bulk_save_objects(objects)


def upsert_book_dicts(records: Iterator[Dict[str, Any]]):
    ses = init_session()

    def is_new(record: Dict[str, Any]) -> bool:
        count = (
            ses.query(UserPurseBook)
            .filter(
                UserPurseBook.user_id == record["user_id"],
                UserPurseBook.asin == record["asin"],
            )
            .count()
        )
        return count == 0

    new_records = []
    update_records = []
    for r in records:
        if is_new(r):
            new_records.append(r)
        else:
            existed = (
                ses.query(UserPurseBook)
                .filter(
                    UserPurseBook.user_id == r["user_id"],
                    UserPurseBook.asin == r["asin"],
                )
                .one()
            )
            if (
                r["title"] != existed.title
                or r["author"] != existed.author
                or (r["image_src"] is not None and r["image_src"] != existed.image_src)
            ):
                r["id"] = existed.id
                r["updated_at"] = make_now()
                update_records.append(r)

    ses.bulk_save_objects([UserPurseBook(**r) for r in new_records])
    ses.bulk_update_mappings(UserPurseBook, update_records)


def select_all(model_class: Type[M]) -> Sequence[M]:
    ses = init_session()
    return ses.query(model_class).all()


def fetch_first(Model) -> Type[M]:
    ses = init_session()
    return ses.query(Model).first()
