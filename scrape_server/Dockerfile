FROM python:3.9

WORKDIR /code

RUN mkdir /code/scrape_server

WORKDIR /code/scrape_server
COPY . .

RUN pip install -r requirements.txt
RUN $(python3 util/__init__.py)
EXPOSE 50051
