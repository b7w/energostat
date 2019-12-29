FROM python:3.8-slim


ENV TIMEZONE="Europe/Moscow"

RUN ln -fs /usr/share/zoneinfo/$TIMEZONE /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update -qq && \
    apt-get install -yqq libc6-dev libssl-dev gcc libxml2-dev libxslt-dev && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get -qq clean

# Copy files
WORKDIR /app

COPY src /app/
COPY pyproject.toml poetry.lock /app/


# Setup
RUN pip3 install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction


ENTRYPOINT ["python"]
CMD ["main.py"]
