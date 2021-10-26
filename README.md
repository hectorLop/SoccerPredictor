# Spanish-LaLiga-Prediction

This projects represents the entire infrastructure to predict the outcome of the Spanish soccer league LaLiga. It includes all the stages of the ML lifecycle, from data ingestion to inference.

<img src="/home/hectorlopez/Datos/Proyectos/Spanish-LaLiga_Prediction/diagram/general_diagram.png" alt="general_diagram"  />

## Tools

- **Dagster**: Used as workflow orchestration tool for the Data Ingestion pipeline, Data Preparation pipeline and the Model training pipeline
- **Scrapy**: Used to scrape the data from the web
- **PostgreSQL**: Used to store the data in its raw form
- **Amazon S3 and DVC**: Data versioning in the cloud. We store in the same repository the data, the training pipeline and the model.
- **MLflow:** Used to keep track of the model training experiments.
- **Streamlit:** Used to create a web app in order to show a demo of the project.

## Environment Variables

| Environment Variables |
| :-------------------- |
| AWS_ACCESS_KEY_ID     |
| AWS_BUCKET            |
| AWS_REGION            |
| AWS_SECRET_ACCESS_KEY |
| DB_HOST               |
| DB_PASSWORD           |
| DB_USER               |

## Docker

There is a `docker-compose.yml` file that defines the services for the web app, the postgres database and the MLflow tracking server. Actually it is running on an Amazon EC2 instance.

The following command will build and start all the services.

```bash
docker-compose up -d --build
```

## To Do

- [ ] Automate the pipeline to be started when new the web page is updated with a new match outcome
- [ ] Create other features in order to improve the results
- [ ] Integrate soccer leagues from other countries
- [ ] ...

