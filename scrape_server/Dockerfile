FROM python:3.9

WORKDIR /code

RUN mkdir /code/scrape_server

WORKDIR /code/scrape_server
COPY . /code/scrape_server/
# COPY scrape_server/requirements.txt ./
# COPY scrape_server/util.py ./

RUN pip install -r requirements.txt
RUN $(python3 util.py)
# RUN python3 server.py &
EXPOSE 50051
# RUN python server.py
# CMD [ "python", "server.py" ]
