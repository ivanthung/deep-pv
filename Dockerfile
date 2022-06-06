FROM --platform=linux/x86_64 python:3.7.13-buster

COPY models /models
COPY deep_pv /deep_pv
COPY requirements.txt /requirements.txt
COPY setup.py /setup.py
COPY scripts /scripts
COPY Makefile /Makefile

RUN pip install --upgrade pip
RUN pip3 install Cython
RUN pip install -r requirements.txt
RUN pip install . -U

CMD uvicorn api.fast:app --host 0.0.0.0 -port $PORT
