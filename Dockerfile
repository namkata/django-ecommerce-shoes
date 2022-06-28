FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN apt-get update
# RUN apt-get install -y libpq-dev
# RUN apt-get install -y build-dep python-psycopg2
# RUN apt-get install -y postgresql-client
# RUN apt install -y netcat
# RUN apt-get install -y libmariadb-dev-compat libmariadb-dev
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends gcc \
#     && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip
COPY requirements.txt /code/
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install psycopg2
COPY . /code/