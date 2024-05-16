from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import random

CATEGORIES = {
    "Fruit": ["apple", "banana", "orange", "pear", "kiwi"],
    "Bakery": ["bread", "croissant", "baguette", "cake"],
    "Drink": ["water", "soda", "beer", "wine"]
}

def generate_product():
    category, products = random.choice(list(CATEGORIES.items()))
    product_name = random.choice(products)
    price = round(random.uniform(0.5, 10.0), 2)
    return {
        "id": str(random.randint(100000000, 999999999)),
        "name": product_name,
        "price": price,
        "category": category
    }

def generate_data():
    store_name = random.choice(["Brussels", "Antwerp", "Ghent", "Leuven", "Bruges"])
    purchase_id = str(random.randint(100000000, 999999999))
    date = "2024-05-16"  
    products = [generate_product() for _ in range(random.randint(1, 5))]

    return {
        "id": purchase_id,
        "store": store_name,
        "date": date,
        "products": products
    }

def send_data_to_api():
    data = generate_data()
    response = requests.post("http://localhost:8000/data", json=data)
    if response.status_code != 200:
        print(f"Request failed with status code {response.status_code}")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 16),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'generate_data_dag',
    default_args=default_args,
    description='A simple DAG to generate and send shopping data',
    schedule_interval=timedelta(seconds=10),
)

send_data_task = PythonOperator(
    task_id='send_data_to_api',
    python_callable=send_data_to_api,
    dag=dag,
)

send_data_task
