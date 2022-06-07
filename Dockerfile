FROM --platform=linux/x86_64 python:3.7.13-buster

COPY api /api
COPY models /models
COPY deep_pv /deep_pv
COPY requirements.txt /requirements.txt
COPY setup.py /setup.py
COPY deeppv-351812-304b34825c68.json /deeppv-351812-304b34825c68.json
COPY .env /.env

RUN pip install --upgrade pip
RUN pip3 install Cython
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
