# [wantas](https://www.wantas.net/search)

### **_ユーザーの"すぐ欲しい"実現アプリ_**

ユーザーが商品を検索し、位置情報から近くのコンビニを特定、商品を表示する。コンビニの商品は地域で差異があるためその点も考慮し、そのコンビニで販売されている商品のみを表示する。
横にグーグルマップも付けているのですぐ行くことができます。


# 使用技術

### プログラミング言語: バックエンド
* Python
* Go
 
### プログラミング言語: フロントエンド
* Html
* Javascript

### データベース
* Sqlite

### CI/CD, VCS
* AWS
* Docker
* GRPC
* Jenkins
* Git

# 技術の選定理由
コンビニの位置情報や商品情報のスクレイピングをするためにPythonを選択しました。WebサーバーはGoのWebフレームワークであるGinで実装し、Goからメソッドを呼び出すようにpythonの機能を使用できるのでGRPCを選択しました。データベースは手軽に操作できるのでSqliteを使用しました。アプリ起動を簡単及び統括的にするためdockerを使用し、docker-composeで起動します。またCI/CDを実装するためにJenkins,AWSを使用しコード編集→git push→jenkinsが自動でテスト→テスト成功したらawsにデプロイという流れを実装しています。またほとんどの関数にテストコードを記述しています。
今後はログイン機能を追加し、SNSでシェアするような機能を付けていきたいと思っています。


# テスト
```shell
docker build -t <image name> . # dockerfileのビルド

docker-compose up -d # 通常時

docker-compose up --build # 通常実行でエラーが出た場合

docker-compose down -v --rmi all # docker-compose終了時
```


### pytestを使用してスクレイピング等が正常に動作しているか確認する
```shell
cd scrape_server
python3 util.py
export SSL_CERT_FILE=/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/certifi/cacert.pem
# 上の出力を貼り付ける。スクレイピングできるようにするために。
export SSL_CERT_FILE=/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/certifi/cacert.pem
pytest -v -p no:warning
```

### webサーバとスクレイピングサーバを起動し、最終テストを行う。

```shell
# 別のセッション
cd scrape_server
python3 server.py

# 別のセッション
cd scrape_client
go run main.go

# 別のセッション
cd scrape_client
go test -v
```

