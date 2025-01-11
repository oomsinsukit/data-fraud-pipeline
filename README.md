# Fraud Detection Data Pipeline

This project demonstrates a **Fraud Detection Data Pipeline** using modern data engineering tools and machine learning. The pipeline identifies fraudulent transactions in real-time and saves the results to a PostgreSQL database. It integrates seamlessly with tools like **Apache Kafka**, **Airflow**, **Docker Compose**, and **Confluent**.

## Table of Contents

- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Architecture](#architecture)
- [Features](#features)
- [Folder Structure](#folder-structure)

---

## Overview

The Fraud Detection Data Pipeline is a scalable solution for detecting fraudulent transactions in real-time. It ingests transaction data via **Kafka**, processes it with a pre-trained **Machine Learning (ML) model**, and stores the results in a PostgreSQL database for further analysis. 

The pipeline is managed by **Apache Airflow**, ensuring a robust and automated workflow.

---

## Technologies Used

- **Apache Kafka**: For real-time data streaming and messaging.
- **Apache Airflow**: For orchestrating tasks in the pipeline.
- **Docker Compose**: For containerizing and managing the services.
- **PgAdmin and PostgreSQL**: For managing and storing transaction data.
- **Confluent Kafka**: For an enhanced Kafka setup.
- **Python (joblib, numpy, psycopg2)**: For ML model inference and database interactions.
- **Machine Learning**: A trained model to predict fraudulent transactions.

---

## Dataset

The fraud detection model was trained using the [Credit Card Fraud Detection Dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) available on Kaggle. This dataset contains real-world transaction data, including 284,807 transactions, of which 492 are fraudulent.

---

## Architecture

### Workflow
1. **Transaction Data Stream**: Kafka producers stream transaction data to the `transactions` topic.
2. **Fraud Detection**: 
    - Airflow DAG consumes the data.
    - Data is cleaned and passed to a pre-trained ML model for fraud prediction.
    - Results are sent to the `fraud_alerts` Kafka topic.
3. **Result Storage**:
    - The pipeline consumes the `fraud_alerts` topic.
    - Results are stored in a PostgreSQL database.
4. **Visualization**: PostgreSQL data can be queried and analyzed through PgAdmin.

---

## Features

- **Real-time Processing**: Detect fraud from streaming transaction data.
- **Scalable**: Supports high throughput with Kafka and PostgreSQL.
- **Automated Workflow**: Managed by Airflow DAGs.
- **Containerized Deployment**: Fully deployable using Docker Compose.

---
