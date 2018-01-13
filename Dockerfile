FROM python:2.7

ENV PYTHONPATH=$PYTHONPATH:/app/

RUN apt-get update
RUN apt-get install -y libav-tools
RUN rm -rf /var/lib/apt/lists/*
RUN mkdir /app
COPY . /app/
WORKDIR /app
RUN pip install .

CMD ["rsdc"]