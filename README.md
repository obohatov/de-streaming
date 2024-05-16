# Delhaize Data Pipeline Project

## Overview

This project implements a data pipeline for Delhaize, a retail company. The pipeline collects shopping data, processes it, and stores it in a cloud database for analytics. The main components of the project are:

1. **API**: Receives shopping data and sends it to a Kafka queue.
2. **Consumer**: Processes the data from Kafka and stores it in a cloud database.
3. **Airflow DAG**: Generates random shopping data and sends it to the API at high frequency.
4. **Kafka**: Message broker for decoupling data producers and consumers.
5. **Cloud Database**: Stores processed data for analytics.

## Architecture Diagram

```
+----------------+       +---------+       +----------+       +-------------------+
|                |       |         |       |          |       |                   |
|  Airflow DAG   +------->  API    +------->  Kafka   +------->  Consumer          |
|                |       |         |       |          |       |                   |
+----------------+       +---------+       +----------+       +-------------------+
                                                                 |
                                                                 |
                                                                 v
                                                       +-------------------+
                                                       |                   |
                                                       |  Cloud Database   |
                                                       |                   |
                                                       +-------------------+
```

## Components

### 1. API

The API is built using FastAPI. It receives shopping data and sends it to a Kafka queue.

#### Example API Request

```json
{
    "id": "123456789",
    "store": "Brussels",
    "date": "2020-01-01",
    "products": [
        {
            "id": "123456789",
            "name": "Banana",
            "price": 1.5
        },
        {
            "id": "123456789",
            "name": "Bread",
            "price": 1.5
        },
        {
            "id": "123456789",
            "name": "Water",
            "price": 1.5
        }
    ]
}
```

### 2. Consumer

The consumer processes the data from Kafka, categorizes the products, calculates the total price, and stores the processed data in a cloud database.

### 3. Airflow DAG

The Airflow DAG generates random shopping data at a high frequency and sends it to the API for testing the system's load handling capabilities.

### 4. Kafka

Kafka is used as a message broker to decouple data producers (API) and consumers (Consumer).

### 5. Cloud Database

Amazon RDS database stores the processed data for analytics.

## Setup

### Prerequisites

- Docker
- Docker Compose
- Python 3.8+
- Virtual Environment (optional but recommended)

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-repo/de-streaming.git
    cd de-streaming
    ```

2. **Create and activate a virtual environment** (optional):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run Kafka with Docker Compose**:
    ```bash
    docker-compose up -d
    ```

5. **Create Kafka topics**:
    ```bash
    docker-compose exec kafka kafka-topics.sh --create --topic delhaize_shop --bootstrap-server localhost:9092
    docker-compose exec kafka kafka-topics.sh --create --topic delhaize_shop_2 --bootstrap-server localhost:9092
    ```

6. **Run the API**:
    ```bash
    uvicorn api.api:app --reload
    ```

7. **Run the Consumer**:
    ```bash
    python consumer.py
    ```

8. **Run Airflow**:
    ```bash
    airflow db init
    airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
    airflow webserver --port 8080
    airflow scheduler
    ```

## Testing

### Unit Tests

Run the unit tests using `pytest`:

```bash
pytest
```

### Stress Test

Run the stress test to send 1000 requests to the API:

```bash
python stress_test.py
```

### Verify Data

Verify that the data is correctly stored in the cloud database:

```bash
python verify_data.py
```

## CI/CD

The project includes a GitHub Actions workflow to run the tests on every push or pull request.

### GitHub Actions

The project includes a GitHub Actions workflow to run the tests on every push or pull request. The workflow is defined in `.github/workflows/ci.yml`.

#### `.github/workflows/ci.yml`

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest
```

## Reproducibility

### Requirements

All dependencies are listed in the `requirements.txt` file. To install the dependencies, run:

```bash
pip install -r requirements.txt
```

### Makefile

A `Makefile` is provided to simplify common tasks. The `make run` target starts the API server.

#### `Makefile`

```makefile
.PHONY: run test

run:
	uvicorn api.api:app --reload

test:
	pytest
```

### Docker

The project includes a `Dockerfile` and `docker-compose.yml` for containerization.

#### `Dockerfile`

```Dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### `docker-compose.yml`

```yaml
version: '3.8'

services:
  zookeeper:
    image: wurstmeister/zookeeper:3.4.6
    ports:
      - "2181:2181"

  kafka:
    image: wurstmeister/kafka
    ports:
      - "9092:9092"
    expose:
      - "9093"
    environment:
      KAFKA_ADVERTISED_LISTENERS: INSIDE://kafka:9093,OUTSIDE://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INSIDE:PLAINTEXT,OUTSIDE:PLAINTEXT
      KAFKA_LISTENERS: INSIDE://0.0.0.0:9093,OUTSIDE://0.0.0.0:9092
      KAFKA_INTER_BROKER_LISTENER_NAME: INSIDE
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_CREATE_TOPICS: "delhaize_shop:1:1,delhaize_shop_2:1:1"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - kafka
```

### Logging

Logging statements are added at strategic points in the code to help with debugging and monitoring.

#### Example Logging in `consumer.py`

```python
import logging
from kafka import KafkaConsumer
from CloudManager import CloudManager
import json

logging.basicConfig(level=logging.INFO)

def process_message(message):
    logging.info(f"Processing message: {message}")
    # Process the message and store in the cloud database
    # ...

consumer = KafkaConsumer(
    'delhaize_shop',
    'delhaize_shop_2',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    process_message(message.value)
```

## Conclusion

This project demonstrates a complete data pipeline for processing shopping data using modern tools and best practices. The pipeline is designed to be robust, scalable, and easy to maintain. By following the steps outlined in this README, you can set up and run the pipeline on your local machine or deploy it to a cloud environment.

## Future Work

- **Scalability**: Implement horizontal scaling for the API and consumer services.
- **Monitoring**: Integrate monitoring tools like Prometheus and Grafana.
- **Security**: Add authentication and authorization for the API.
- **Data Validation**: Implement data validation and error handling mechanisms.

Feel free to contribute to this project by submitting pull requests or opening issues on GitHub.

This project was created by Oleh Bohatov and Mahak Behl ([LinkedIn](https://www.linkedin.com/in/mahak-behl-48541a16a/), [GitHub](https://github.com/MahakBehl))
