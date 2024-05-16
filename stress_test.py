import random
from requests import Session

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
    date = "2020-01-01"  # fixed date for simplicity
    products = [generate_product() for _ in range(random.randint(1, 5))]

    return {
        "id": purchase_id,
        "store": store_name,
        "date": date,
        "products": products
    }

with Session() as sess:
    for i in range(1000):
        data = generate_data()
        response = sess.post("http://localhost:8000/data", json=data)
        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}")

print("Stress test completed.")
