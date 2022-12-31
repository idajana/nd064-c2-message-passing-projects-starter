import grpc
import location_pb2
import location_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

channel = grpc.insecure_channel("localhost:30008")
stub = location_pb2_grpc.LocationServiceStub(channel)

print("Testing location creation.")

location = location_pb2.LocationMessage(
    person_id=6,
    latitude=200,
    longitude=300

)

response = stub.Create(location)
print(response)