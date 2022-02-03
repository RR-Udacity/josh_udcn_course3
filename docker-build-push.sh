# build api & push to docker hub
cd ~/git/udcn_course3/modules/api
docker build -t jdhaines/udaconnect-api:latest .
docker push jdhaines/udaconnect-api

# build locationProducer & push to docker hub
cd ~/git/udcn_course3/modules/locationProducer
docker build -t jdhaines/udaconnect-locationproducer:latest .
docker push jdhaines/udaconnect-locationproducer

# build locationConsumer & push to docker hub
cd ~/git/udcn_course3/modules/locationConsumer
docker build -t jdhaines/udaconnect-locationconsumer:latest .
docker push jdhaines/udaconnect-locationconsumer

# redeploy the k8s cluster services with new images
cd ~/git/udcn_course3/
kubectl apply -f deployment/

# delete pods to force re-pull of new images
kubectl delete pods -l service=udaconnect-api
kubectl delete pods -l service=udaconnect-locationproducer
kubectl delete pods -l service=udaconnect-locationconsumer
# kubectl logs -f -l service=udaconnect-api
