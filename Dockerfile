FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN cd /app

RUN poetry install --no-root

RUN pip install -r requirements.txt

RUN cd server

EXPOSE 8080

CMD ["uvicorn", "server.ExpandReduceFlow:app", "--host", "0.0.0.0", "--port", "8080"]
