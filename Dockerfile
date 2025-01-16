FROM debian:latest

RUN apt update && apt install -y cron curl python3 python3-pip python3-poetry


ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY . ./

RUN poetry install

RUN echo "*/1 * * * * cd /app && python3 update.py >> /var/log/cron.log 2>&1" \
    > /etc/cron.d/mycron && \
    chmod 0644 /etc/cron.d/mycron && \
    crontab /etc/cron.d/mycron

RUN touch /var/log/cron.log

CMD ["cron", "-f"]
