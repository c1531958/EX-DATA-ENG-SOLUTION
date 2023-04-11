FROM python:3.9.16-buster

WORKDIR /usr/app/src
COPY src/ ./

RUN pip install -r requirements.txt

CMD [ "python", "./main.py"]
