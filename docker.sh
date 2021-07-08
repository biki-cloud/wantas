docker stop scrape_server_container
docker rm scrape_server_container
docker rmi scrape_server_image

docker build -t scrape_server_image .

docker run -it --name scrape_server_container -d -p 50051:50051 scrape_server_image

docker exec -it scrape_server_container bash

docker stop scrape_client_container
docker rm scrape_client_container
docker rmi scrape_client_image

docker build -t scrape_server_image .

docker run -it --name scrape_server_container -d -p 50051:50051 scrape_server_image

docker exec -it scrape_server_container bash