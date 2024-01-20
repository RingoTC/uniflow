FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN cd /app

RUN poetry install --no-root

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "/app/cloud/hello.py"]