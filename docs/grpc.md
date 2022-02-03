# gRPC Documentation

To test location functionality for gRPC and Kafka:

```bash
# Run project as originally intended
# Re-Run deploy for new services in my project
kubectl deploy -f deployment/

# get pods
kubectl get po

# copy name of udaconnect-locationproducer pod
kubectl exec -it udaconnect-locationproducer-xxx -- sh

# run the writer script to generate 4 location items and send them via gRPC
python writer.py

# If you watch the database before and after you'll see the items added

# You can also watch the logs on the udaconnect-locationconsumer which is watching
# the kafka queue and see the new items come through
kubectl logs -f svc/udaconnect-locationconsumer
```
