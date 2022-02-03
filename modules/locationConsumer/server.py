import logging
from kafka import KafkaConsumer
import psycopg2
import os
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-locationConsumer")

consumer = KafkaConsumer("locationTopic", bootstrap_servers=['kafka-service:9092'])

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def consume_locations():
    while True:
        for item in consumer:
            item = item.value
            item = json.loads(item)
            add_location_to_db(item)


def add_location_to_db(locationItem):
    try:
        conn = psycopg2.connect(
            user=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_NAME,
            port=DB_PORT,
        )

        cur = conn.cursor()

        insert = (
            "INSERT INTO location (person_id, coordinate) values (%s, ST_POINT(%s, %s))"
        )

        cur.execute(
            insert,
            (
                int(locationItem["person_id"]),
                float(locationItem["latitude"]),
                float(locationItem["longitude"]),
            )
        ),
        conn.commit()
        logging.debug("{} location added to the db".format(locationItem))
    except Exception as error:
        logging.debug("Error info: {}".format(error))
        logging.debug("Something went wrong on location db insert")


if __name__ == "__main__":
    logging.basicConfig()
    consume_locations()