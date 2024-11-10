FROM python:3.12.7-alpine3.19

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./init.sh .
RUN sed -i 's/\r$//g' /usr/src/app/init.sh
RUN chmod +x /usr/src/app/init.sh

COPY . .

# Install docker-cli
RUN apk add --update docker openrc
RUN rc-update add docker boot

# Setup cron
RUN echo '*/30 * * * *    python /usr/src/app/manage.py refresh_characters' > /etc/crontabs/root

ENTRYPOINT ["/usr/src/app/init.sh"]
