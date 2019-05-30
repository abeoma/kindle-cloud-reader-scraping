# ローカル開発構築手順
```
> pwd
path/to/kindle-scraping

# mysql起動
> docker-compose up

# pip install
> pip3 install docker/python/requirements.txt

# masterDB作成
> ./goose-masterdb.sh up

# SQLAlchemy model自動生成
> ./generate-models.sh
```

# スクレイピングテスト
### 1. test.pyの下記項目に文字列を記入
```
email = "" <- Kindleアカウントのメールアドレス
password = "" <- Kindleアカウントのパスワード
name = ""
```
※データベースには暗号化されたパスワードが保管されます

### 2. test.pyを実行
```
> pwd
path/to/kindle-scraping

> cd src
> ./python.sh test.py
```

### 3. データの確認
データベースに書籍の一覧が取り込まれているか確認
