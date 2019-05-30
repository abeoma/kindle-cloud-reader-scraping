from typing import Dict

from lib.helper import new_pk
from cli.import_to_masterdb.common import insert_dict
from lib.crypt import AESCipher
from models.master_models_generated import User


def import_user(email: str, password: str, name: str):
    cipher = AESCipher(email)
    encrypt_password = cipher.encrypt(password)
    record: Dict[str, str] = dict(
        id=new_pk(), email=email, password=encrypt_password, name=name
    )
    insert_dict(record, User)
