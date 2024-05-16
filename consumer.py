import json
from kafka import KafkaConsumer
from CloudManager import CloudManager, get_category
import logging

logging.basicConfig(level=logging.INFO)

consumer = KafkaConsumer(
    'shop_data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

cloud_manager = CloudManager()
cloud_manager.connect()
cloud_manager.create_tables()

for message in consumer:
    data = message.value
    logging.info(f"Received message: {data}")
    purchase_id = data['id']
    store = data['store']
    date = data['date']
    total_price = sum([product['price'] for product in data['products']])

    logging.info(f"Processing purchase: {purchase_id} at {store} on {date} with total price {total_price}")

    try:
        cloud_manager.insert_purchase(purchase_id, store, date, total_price)
    except Exception as e:
        logging.error(f"Failed to insert purchase: {e}")

    for product in data['products']:
        product_id = product['id']
        name = product['name']
        price = product['price']
        category = get_category(name)

        logging.info(f"Inserting product {name} with category {category}")
        try:
            cloud_manager.insert_product(product_id, purchase_id, name, price, category)
        except Exception as e:
            logging.error(f"Failed to insert product: {e}")

cloud_manager.close()
