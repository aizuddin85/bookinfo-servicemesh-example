# Bookinfo Service Mesh Example (OpenShift 4)

This example based on https://docs.openshift.com/container-platform/4.3/service_mesh/service_mesh_day_two/ossm-example-bookinfo.html.

We take those configurations object and splitted into each type.


Assuming service mesh already being installed and running as per: https://docs.openshift.com/container-platform/4.3/service_mesh/service_mesh_install/preparing-ossm-installation.html


In high level, 

   - Deploy details, productpage, ratings and reviews service.
   - Configure istio ingressgateway and virtual service
   - Configure istio DestionationRule for each of the service with mTLS.


1. Checkout this repo:
     
   ```#> git clone git@github.com:aizuddin85/bookinfo-servicemesh-example.git```

2. Change directory to `bookinfo`:  
   
   ```
   #> cd bookinfo-servicemesh-example/bookinfo
   #> ll
   total 4
    drwxr-xr-x. 2 mzali mzali  68 Feb 28 16:05 details
    drwxr-xr-x. 2 mzali mzali 125 Feb 28 16:11 productpage
    drwxr-xr-x. 2 mzali mzali  71 Feb 28 16:01 ratings
    -rw-r--r--. 1 mzali mzali 228 Feb 28 18:34 README.md
    drwxr-xr-x. 5 mzali mzali 108 Feb 28 16:05 reviews
    drwxr-xr-x. 2 mzali mzali 158 Feb 28 18:30 servicemesh-destinationrules
    drwxr-xr-x. 2 mzali mzali  47 Feb 28 16:15 servicemesh-gateway
    drwxr-xr-x. 2 mzali mzali  54 Feb 28 16:15 servicemesh-virtualservice

    ```

3. Create new project call `bookinfo`:  
   
   ```
   #> oc new-project bookinfo
    Now using project "bookinfo" on server "https://api.ocp.example.com:6443".

    You can add applications to this project with the 'new-app' command. For example, try:

    oc new-app django-psql-example

    to build a new example application in Python. Or use kubectl to deploy a simple Kubernetes application:

    kubectl create deployment hello-node --image=gcr.io/hello-minikube-zero-install/hello-node
    ```


4. Deploy `details` service:  
   
   ```
    #> cd details
    #> oc create -f details-service.yaml -f details-v1-deployment.yaml
    #> oc get pods
    NAME                          READY   STATUS              RESTARTS   AGE
    details-v1-85dc45d497-ng5w9   0/2     ContainerCreating   0          9s
   ```

5.  Deploy `ratings` service:  
   
    ```
    #> cd ../ratings/

    #> ls
    ratings-v1-deployment.yaml  ratings-v1-service.yaml

    #> oc create -f ratings-v1-deployment.yaml -f ratings-v1-service.yaml
    deployment.apps/ratings-v1 created
    service/ratings created
    ```


6.  Deploy `reviews` service (v1,v2 and v3):  

    ```
    #> cd ../reviews/
    
    #> ls
    bookinfo-reviews-serviceaccount.yaml  reviews-service.yaml  v1  v2  v3

    #> oc create  -f bookinfo-reviews-serviceaccount.yaml -f reviews-service.yaml -f v1/reviews-v1-deployment.yaml -f v2/reviews-v2-deployment.yaml -f v3/reviews-v3-deployment.yaml 
    serviceaccount/bookinfo-reviews created
    service/reviews created
    deployment.apps/reviews-v1 created
    deployment.apps/reviews-v2 created
    deployment.apps/reviews-v3 created
    ```

7. Deploy `productpage` service:
   
   ```
   #> cd ../productpage/
   #> ll
   total 12
   -rw-r--r--. 1 mzali mzali  74 Feb 28 16:10 bookinfo-productpage-serviceaccount.yaml
   -rw-r--r--. 1 mzali mzali 192 Feb 28 16:11 productpage-service.yaml
   -rw-r--r--. 1 mzali mzali 607 Feb 28 16:11 productpage-v1-deplopyment.yaml
   #> oc create  -f bookinfo-productpage-serviceaccount.yaml -f productpage-service.yaml  -f productpage-v1-deplopyment.yaml
   serviceaccount/bookinfo-productpage created
   service/productpage created
   deployment.apps/productpage-v1 created
   ```


8. Now, lets define service mesh gateway for `bookinfo` apps:
   ```
    #> cd ../servicemesh-gateway/

    #> ls
    bookinfo-servicemesh-gateway.yaml

    #> oc create  -f bookinfo-servicemesh-gateway.yaml 
    gateway.networking.istio.io/bookinfo-gateway created
   ```

9.  At this stage we have already exposed `bookinfo` from service mesh via gateway defined above. Next, we need to create virtualservice for the gateway:
    
    ```
    #> cd ../servicemesh-virtualservice/

    #> ls
    bookinfo-servicemesh-virtualservice.yaml

    #> oc create  -f bookinfo-servicemesh-virtualservice.yaml 
    virtualservice.networking.istio.io/bookinfo created
    ```
10. Next find and defined the `GATEWAY_URL` so we can test using `cURL`.
    
    ```
    #> export GATEWAY_URL=$(oc -n istio-system get route istio-ingressgateway -o jsonpath='{.spec.host}')

    #> echo $GATEWAY_URL
    istio-ingressgateway-istio-system.apps.example.com
    ```
11. Now ensure all pods are running for `bookinfo`:
    
    ```
    #> oc get pods -n bookinfo
    NAME                              READY   STATUS    RESTARTS   AGE
    details-v1-85dc45d497-ng5w9       2/2     Running   0          23m
    productpage-v1-5fc4d7dbc9-4t7bx   2/2     Running   0          8m56s
    ratings-v1-6db7864765-lq7vl       2/2     Running   0          20m
    reviews-v1-7464fbc59d-4blvp       2/2     Running   0          11m
    reviews-v2-569f769b5b-p7w79       2/2     Running   0          11m
    reviews-v3-b8985f85d-swtcl        2/2     Running   0          11m
    ```


12. Now lets hit the URL:

    ```
    #> curl -o /dev/null -s -w "%{http_code}\n" http://$GATEWAY_URL/productpage
    200
    ```
When response code is `200` this mean a succesful depolyment and traffic is properly router in service mesh data plane.


Inspect one of the pod, and you will see there is `istio-proxy` containers being injected by service mesh:

```
#> oc get  pods details-v1-85dc45d497-ng5w9 -o jsonpath={.spec.containers[*].name}
details istio-proxy
```