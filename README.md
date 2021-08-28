# [wantas](https://www.wantas.net/search)

### **_ユーザーの"すぐ欲しい"実現アプリ_**

ユーザーが商品を検索し、位置情報から近くのコンビニを特定、商品を表示する。コンビニの商品は地域で差異があるためその点も考慮し、そのコンビニで販売されている商品のみを表示する。
横にグーグルマップも付けているのですぐ行くことができます。


# 使用技術

### プログラミング言語: バックエンド
* Python
* Go
* Shell
 
### プログラミング言語: フロントエンド
* Html
* Css
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


# とりあえずローカルで使ってみる
### 起動方法
```shell
git clone git@github.com:biki-cloud/wantas.git
docker-compose up -d # 起動
```

### [**アクセス**](http://localhost:80/search)

### 終了方法
```shell
docker-compose down -v --rmi all # 終了
```

# テスト
```shell
# 起動
docker-compose up -d # 通常起動。エラーが出た場合は-dを--buildに変えてみる。

# pytestを使用してスクレイピング等が正常に動作しているか確認する
cd scrape_server
python3 util.py
# 上の出力をコマンドラインに貼り付け実行する。スクレイピングできるようにするために。
pytest -v -p no:warning

# webサーバとスクレイピングサーバを起動し、最終テストを行う。
# 別のセッション
cd scrape_server
python3 server.py

# 別のセッション
cd scrape_client
go run main.go

# 別のセッション
cd scrape_client
go test -v

# 終了
docker-compose down -v --rmi all # docker-compose終了時
```

# プロファイリング
プロファイリングはcProfileを使用する。使用方法は以下の通り。
```python
import cProfile
import time

def f():
    print("start")
    time.sleep(2)
    print("end")

cProfile.run('f()')
```
出力結果
```text
start
end
         7 function calls in 2.003 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    2.003    2.003 <string>:1(<module>)
        1    0.000    0.000    2.003    2.003 time_test.py:5(f)
        1    0.000    0.000    2.003    2.003 {built-in method builtins.exec}
        2    0.000    0.000    0.000    0.000 {built-in method builtins.print}
        1    2.003    2.003    2.003    2.003 {built-in method time.sleep}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

