FROM python:3.7

RUN apt-get update
RUN apt-get install git
RUN git clone https://github.com/hectorLop/Spanish-LaLiga-Prediction.git app/

RUN pip install streamlit
RUN pip install boto3
RUN pip install pandas
RUN pip install python-dotenv

EXPOSE 8501

WORKDIR /app