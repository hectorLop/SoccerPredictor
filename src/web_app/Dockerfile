FROM python:3.7

RUN apt-get update

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install streamlit

COPY src app/src
COPY logs app/logs

ENV PYTHONPATH "${PYTHONPATH}:/app"

WORKDIR /app

EXPOSE 8501

CMD ["streamlit", "run", "src/web_app/web_app.py"]