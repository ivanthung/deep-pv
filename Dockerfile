FROM --platform=linux/x86_64 python:3.7.13-buster

COPY models /models
COPY deep_pv /deep_pv
COPY requirements.txt /requirements.txt
COPY setup.py /setup.py

RUN pip install --upgrade pip
RUN pip3 install Cython
RUN pip install -r requirements.txt

CMD uvicorn api.fast:app --host 0.0.0.0
