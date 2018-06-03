FROM python:3.6.3-slim

RUN apt-get update \
  && apt-get install -y gcc \
  && rm -rf /var/lib/apt/lists/*

EXPOSE 8080

ADD . /ticker_tape

WORKDIR /ticker_tape

RUN pip install -r requirements.txt
RUN python setup.py install

WORKDIR /ticker_tape/src/ticker_tape

CMD ["python", "-m", "main"]