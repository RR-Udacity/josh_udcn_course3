# Design Decisions

## Rest

I maintained the REST message system between the frontend and the primary API.  This seems a perfect fit for REST and required only a small amount of refactoring.  The current endpoints needed cleaned up as they didn't work correctly.  I kept the connection and person services in the primary API as the load should be sufficient that they'll work fine there with only REST interaction.

## gRPC

I refactored the location service which seemed to need the most help.  I started with a gRPC service that will take location data in from various clients via gRPC.  This is nice because it's fast and will allow things like mobile phones, other devices, etc. to pass in locations quickly.  This service takes in the location items and passes them into a kafka queue.  This service is called the Location Producer service.

## Kafka

The next service is the Location Consumer service.  This service watches the kafka queue and takes any new location items and stores them in the database.  The queue helps make sure all locations get added even though the database writes may be slower than the services can generate them.  Kafka will help protect this rate difference.  If things get too heavy we can always scale out the database service.