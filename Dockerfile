FROM python:3.8-alpine

RUN adduser -D quickgig

WORKDIR /home/quickgig

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install pymysql[rsa]

COPY app app
COPY migrations migrations
COPY quickgig.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP quickgig.py

RUN chown -R quickgig:quickgig ./
USER quickgig

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
