FROM python:3.12-slim


WORKDIR /app

# for psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev


COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
