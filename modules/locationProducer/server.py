import logging
import grpc
from concurrent import futures
import location_pb2
import location_pb2_grpc
from kafka import KafkaProducer
import json


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-locationProducer")

producer = KafkaProducer(bootstrap_servers=['kafka-service:9092'])

class LocationProcessor(location_pb2_grpc.LocationProcessor):
    def Create(self, req, ctx):
        logging.debug("New Location Item")
        new_item = {
            "person_id": req.person_id,
            "latitude": req.latitude,
            "longitude": req.longitude,
        }
        logging.debug("Item: {}".format(new_item))
        producer.send('locationTopic', json.dumps(new_item).encode('utf-8'))
        producer.flush()
        return location_pb2.LocationItem(**new_item)

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
  location_pb2_grpc.add_LocationProcessorServicer_to_server(
      LocationProcessor(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  print("Server Started and waiting on 50051...")
  server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()
