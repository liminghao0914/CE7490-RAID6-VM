FROM python:3.9

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir kademlia
RUN pip install --no-cache-dir asyncio
RUN pip install --no-cache-dir flask
RUN pip install --no-cache-dir requests


EXPOSE 5000
EXPOSE 8468

CMD [ "python", "app.py" ]
