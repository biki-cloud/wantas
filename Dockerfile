FROM python:3.9

WORKDIR /code

RUN mkdir /code/scrape_server

WORKDIR /code/scrape_server
# COPY scrape_server/* /code/scrape_server/
# COPY scrape_server/requirements.txt ./
# COPY scrape_server/util.py ./

# RUN pip install -r requirements.txt
# RUN $(python3 util.py)
# RUN python3 server.py