docker stop test_con
docker rm test_con
docker rmi test_img

docker build -t test_img .

# docker run -it --name scrape_server -v scrape_server:/code -d scrape_server
docker run -it --name test_con -v scrape_server:/code/scrape_server -d -p 50051:50051 test_img

docker exec -it test_con bash