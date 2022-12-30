# stock-closing-price-api

simple rest api for stock closing price

## context and summary

This API fetches stock data from an upstream API, and does some formatting and calculation before returning the result.

Two important parameters are NDAYS and SYMBOL. Both are passed as env variables in k8s and have defaults for running directly or via Docker if they are not set.

SYMBOL => company stock symbol
NDAYS => number of days

The data is trimmed to NDAYS (or less if the data doesn't exist) for SYMBOL. The average closing price is calculated for the dataset and appended as it's own field.
The metadata from the upstream API is also returned.

## build and run locally with Docker

### build

run `build-docker-local.sh`

### run

run `run-docker-local.sh`

## run with kubernetes locally

spin up minikube, docker-desktop, etc

```
cd k8s
kubectl create -f stock-closing-price-api-env.yaml
kubectl create -f stock-closing-price-api-secret.yaml
kubectl apply -f stock-closing-price-api-deployment.yaml
kubectl port-forward deployment/stock-closing-price-api 5000
```
## test with curl

```
curl localhost:5000/
```

or

```
curl localhost:5000/stockprice/
```

This will only work with k8s locally if the port-forward is running.

## updating the image, adding and deploying a change

Build the image, and set the tag version to a release that follows semantic versioning (major.minor.patch)
```
docker build --tag "${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:0.0.4" .
```

Once the build succeeds locally, push it to the docker registry (could easily be artifactory, etc).
The example here is pushing to Docker hub.
```
docker push csuttles/stock-closing-price-api:0.0.4
```

Update the kubernetes deployment's containerspec to use the new version.

In this example line 19 has been edited to include the version we pushed in the previous step.
```
 16     spec:
 17       containers:
 18       - name: stock-closing-price-api
 19         image: csuttles/stock-closing-price-api:0.0.4
 20         ports:
 21         - containerPort: 5000
```


