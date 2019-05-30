from cli.import_to_masterdb.common import fetch_first
from cli.import_to_masterdb.import_user import import_user
from cli.import_to_masterdb.import_user_purse_book import import_user_purse_books
from models.master_models_generated import User

email = ""
password = ""
name = ""


def main():
    import_user(email=email, password=password, name=name)
    user: User = fetch_first(Model=User)
    import_user_purse_books(user=user)


if __name__ == "__main__":
    main()
