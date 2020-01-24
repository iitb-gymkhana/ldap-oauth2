FROM python:2.7

WORKDIR /sso

COPY . .

RUN apt-get update && \
    apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev
RUN pip install -r requirements.txt

CMD gunicorn sso.wsgi:application --bind 0.0.0.0:8000 --workers 3

