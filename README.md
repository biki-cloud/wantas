# wantas


this is wantas


# How to test

docker build -t <image name> . -> dockerfileのビルド

docker-compose up -d -> 通常時

docker-compose up --build -> 通常実行でエラーが出た場合

docker-compose down -v --rmi all -> docker-compose終了時

## 1

cd scrape_server

python3 scrape_server.py

## 2

cd scrape_server

pytest -v -p no:warnings

## 3

cd scrape_client

go run main.go

## 4

cd scrape_client

go test -v




