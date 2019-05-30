# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class GooseDbVersion(Base):
    __tablename__ = 'goose_db_version'

    id = Column(BIGINT(20), primary_key=True, unique=True)
    version_id = Column(BIGINT(20), nullable=False)
    is_applied = Column(TINYINT(1), nullable=False)
    tstamp = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class User(Base):
    __tablename__ = 'users'

    id = Column(String(255), primary_key=True, nullable=False, index=True)
    email = Column(String(255), primary_key=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class CrawlQueue(Base):
    __tablename__ = 'crawl_queues'

    id = Column(String(255), primary_key=True, index=True)
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    priority = Column(INTEGER(10), nullable=False)
    crawl_status = Column(INTEGER(10), nullable=False)
    crawl_error = Column(String(255))
    error_message = Column(String(255))
    crawled_on = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    crawled_end = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship('User')


class UserPurseBook(Base):
    __tablename__ = 'user_purse_books'

    id = Column(String(255), primary_key=True, index=True)
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    asin = Column(String(255), nullable=False)
    title = Column(String(255))
    author = Column(String(255))
    image_src = Column(String(255))
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship('User')
