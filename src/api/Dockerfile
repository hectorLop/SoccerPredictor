FROM python:3.7

RUN apt-get update

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install fastapi uvicorn

COPY src app/src
COPY logs app/logs

ENV PYTHONPATH "${PYTHONPATH}:/app"

WORKDIR /app

EXPOSE 8080

CMD ["uvicorn", "src.api.api:app", "--host", "0.0.0.0", "--port", "8080"]