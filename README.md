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
```
## test with curl

There's a single endpoint, but it's available in more than one route.

```
curl localhost:5000/
```

or

```
curl localhost:5000/stockprice/
```

This will only work with k8s locally if the port-forward is running.

```
kubectl port-forward deployment/stock-closing-price-api 5000 &
```

## updating the image, adding and deploying a change

Build the image, and set the tag version to a release that follows semantic versioning (major.minor.patch)
```
docker build --tag "${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:0.0.5" .
```

Once the build succeeds locally, push it to the docker registry (could easily be artifactory, etc).
The example here is pushing to Docker hub.
```
docker push csuttles/stock-closing-price-api:0.0.5
```

Update the kubernetes deployment's containerspec to use the new version.

In this example line 19 has been edited to include the version we pushed in the previous step.
```
 16     spec:
 17       containers:
 18       - name: stock-closing-price-api
 19         image: csuttles/stock-closing-price-api:0.0.5
 20         ports:
 21         - containerPort: 5000
```


## Resilience

In the current state, this is not a production ready product (not even close).
This is a "proof of concept" level of completion. This section discusses what changes could (and must) be made if this were to become a more resilient version of this service.

### Concerns to address with app itself

There are many concerns to resolve. The first things to fix:

* every get creates a get to the upstream API
* no persistence layer, caching has lots of room for improvement
* limited features in api (response could include cache-control / expiry in headers, no parameters, no pagination, etc)
* might be better to move to a more performant language before putting too much into this (go, java, etc)

### Scaling Out and Architecture Improvements

Once the largest issues are addressed, there's some easy architecture wins:

* scale the deployment beyond a single replica, balance the load across replicas
* assuming there's a persistance layer (frontend/backend model), the backend might need to be scaled to multiple replicas as well
* depending on scale, maybe a read through cache, CDN, multi-region or both is required

### Infrastructure as code

* deployments should not work in prod how they work in this readme
* terraform or similar should be used to provision infra
* infra DSL (terraform or similar) needs to be version controlled
* changes in the git repo should cause infrastructure to be updated (gitops)

### Operational Hygeine 

* monitoring / instrumentation is required
* SLA / SLI / SLIs need to be defined based on data from observabilty tooling
* principle of least privilege for access to systems and usage
* keep clean, actionable logs

### Security Posture

* network traffic needs to also follow principle of least privilege at every layer
* same things for system access and process execution
* vulnerability scanning / static code analysis on repo
* infosec review or equivalent ideally including redteam/pentest
