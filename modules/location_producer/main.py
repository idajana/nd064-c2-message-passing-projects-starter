import time
import os
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc
import json
from kafka import KafkaProducer

kafka_url = os.environ["KAFKA_URL"]
kafka_topic = os.environ["KAFKA_TOPIC"]

producer = KafkaProducer(bootstrap_servers=kafka_url)

class LocationEventServicer(location_pb2_grpc.LocationServiceServicer):

        def Create(self, request, context):

            request_value = {
                 "person_id": request.person_id,
                 "latitude": request.latitude,
                 "longitude": request.longitude,
              }
            print(request_value)
            user_encode_data = json.dumps(request_value, indent=2).encode('utf-8')
            producer.send(kafka_topic, user_encode_data)

            return location_pb2.LocationMessage(**request_value)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationEventServicer(), server)

print("gRPC Server listening on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(500)
except KeyboardInterrupt:
    server.stop(0)