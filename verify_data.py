from CloudManager import CloudManager
import logging

logging.basicConfig(level=logging.INFO)

def main():
    cloud_manager = CloudManager()
    cloud_manager.connect()  
    data = cloud_manager.retrieve_data()
    logging.info(f"Items in the cloud database: {len(data)}")

    cloud_manager.close()

    if len(data) == 1000:
        logging.info("Test successful! All 1000 items are present.")
    else:
        logging.info(f"Test failed! Expected 1000 items, but found {len(data)}.")

if __name__ == "__main__":
    main()
