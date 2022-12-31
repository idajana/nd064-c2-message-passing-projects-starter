import os
import json
import logging

from kafka import KafkaConsumer
from sqlalchemy import create_engine

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
KAFKA_URL = os.environ["KAFKA_URL"]
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=[KAFKA_URL], group_id=None, auto_offset_reset='earliest')
engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)
conn = engine.connect()

for encoded_msg in consumer:
    decoded_msg = encoded_msg.value.decode('utf-8')
    msg_json = json.loads(decoded_msg)

    person_id = int(msg_json["person_id"])
    latitude = int(msg_json["latitude"])
    longitude = int(msg_json["longitude"])
    logging.info(f"Recieved a new location for person with id {person_id}, adding to database...")
    sql_query = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))".format(person_id, latitude, longitude)
    conn.execute(sql_query)


