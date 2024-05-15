import json
from kafka import KafkaConsumer
from CloudManager import CloudManager, get_category  

# Initializing the Kafka consumer
consumer = KafkaConsumer(
    'shop_data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Initializing a database connection
cloud_manager = CloudManager()
cloud_manager.connect()
cloud_manager.create_tables()

# Processing and saving messages
for message in consumer:
    data = message.value
    purchase_id = data['id']
    store = data['store']
    date = data['date']
    total_price = sum([product['price'] for product in data['products']])

    # Inserting Purchase data
    cloud_manager.insert_purchase(purchase_id, store, date, total_price)

    # Inserting Product data
    for product in data['products']:
        product_id = product['id']
        name = product['name']
        price = product['price']
        category = get_category(name)

        cloud_manager.insert_product(product_id, purchase_id, name, price, category)

cloud_manager.close()
