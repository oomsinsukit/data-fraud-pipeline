from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from kafka import KafkaConsumer, KafkaProducer
import numpy as np
import json
import joblib
import psycopg2
from psycopg2.pool import SimpleConnectionPool

default_args = {
    'owner': 'oomsin',
    'start_date': datetime(2023, 9, 3, 10, 00)
}

# PostgreSQL เชื่อมต่อ Pool (สร้าง Pool ไว้เชื่อมต่อ)
postgres_pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host="172.18.0.2",
    database="airflow",
    user="airflow",
    password="airflow"
)

def load_model():
    try:
        model = joblib.load('/opt/airflow/dags/fraud_detection.pkl')
        return model
    except Exception as e:
        print(f"An error occurred: {e}")

def clean_data(data):
    try:
        features = np.array([[data['Time'], data['V1'], data['V2'], data['V3'], data['V4'], data['V5'], data['V6'],\
                            data['V7'], data['V8'], data['V9'], data['V10'], data['V11'], data['V12'], data['V13'],\
                            data['V14'], data['V15'], data['V16'], data['V17'], data['V18'], data['V19'], data['V20'],\
                            data['V21'], data['V22'], data['V23'], data['V24'], data['V25'], data['V26'], data['V27'], data['V28'], data['Amount']]])
        return features
    except KeyError as e:
        print(f"Missing key in data: {e}")
        return None

def start_kafka_consumer(**kwargs):
    consumer = KafkaConsumer(
        'transactions',
        bootstrap_servers='broker:29092',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    producer = KafkaProducer(
        bootstrap_servers='broker:29092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    model = load_model()

    for _ in range(100):
        message = next(consumer)
        data = message.value
        features = clean_data(data)
        prediction = model.predict(features)
        is_fraud = bool(prediction[0])
        print(data)
        print(prediction)

        # ส่งผลลัพธ์ไปยัง Kafka
        producer.send('fraud_alerts', value={'transaction_id': data['Unnamed: 0'], 'fraud': is_fraud}) #ยกตัวอย่าง Unamed: 0 (เป็นเลข index ของข้อมูลซึ่่งไม่ซ้ำกันอยู่แล้ว) เป็น transaction_id

    consumer.close()
    producer.close()

def consumer_and_save_to_postgresql():
    consumer = KafkaConsumer(
        'fraud_alerts',
        bootstrap_servers='broker:29092',
        auto_offset_reset='earliest',
        consumer_timeout_ms=10000,  # Timeout หลังจาก 10 วินาทีที่ไม่มีข้อความใหม่
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    try:
        # เชื่อมต่อกับ PostgreSQL
        conn = postgres_pool.getconn()
        cursor = conn.cursor()

        # สร้างตารางถ้ายังไม่มี
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS fraud_alerts (
            transaction_id VARCHAR(255) PRIMARY KEY,
            fraud BOOLEAN,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()
        
        for message in consumer:
            data = message.value
            transaction_id = data.get('transaction_id', 'unknown')
            is_fraud = data.get('fraud', False)

            # บันทึกข้อมูลลง PostgreSQL
            cursor.execute("""
            INSERT INTO fraud_alerts (transaction_id, fraud)
            VALUES (%s, %s)
            ON CONFLICT (transaction_id) DO NOTHING;
            """, (transaction_id, is_fraud))
            conn.commit()

            print(f"Saved transaction {transaction_id} to PostgreSQL")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            postgres_pool.putconn(conn) #คืน connection สู่ Pool
        consumer.close()

with DAG('fraud_detection_pipeline',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup= False
) as dag:
    streaming_task = PythonOperator(
        task_id = 'start_consumer',
        python_callable = start_kafka_consumer
    )
    save_result_task = PythonOperator(
        task_id = 'save_result_to_postgresql',
        python_callable= consumer_and_save_to_postgresql
    )

streaming_task >> save_result_task
    