FROM python:3.9-alpine

WORKDIR /CyberNadzor

COPY requirements.txt /CyberNadzor/
RUN pip install -r /CyberNadzor/requirements.txt
COPY . /CyberNadzor/

CMD python3 /CyberNadzor/app.py