import logging
import grpc
import location_pb2
import location_pb2_grpc


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("location-writer")

channel = grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),))

stub = location_pb2_grpc.LocationProcessorStub(channel)

item1 = location_pb2.LocationItem(
    person_id=6,
    latitude=45.1234567,
    longitude=-45.1234567
)
item2 = location_pb2.LocationItem(
    person_id=5,
    latitude=35.2,
    longitude=17.1
)
item3 = location_pb2.LocationItem(
    person_id=1,
    latitude=145.1234567,
    longitude=-122.1234567
)
item4 = location_pb2.LocationItem(
    person_id=8,
    latitude=90.1,
    longitude=29.5
)

stub.Create(item1)
stub.Create(item2)
stub.Create(item3)
stub.Create(item4)