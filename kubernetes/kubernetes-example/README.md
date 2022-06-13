# Kubernetes Example

This is a simple example in using Kubernetes and setting up a local cluster using minikube and kubectl. To manage the pods, k9s can also be used to make your life a little easier.

## Architecture
mongodb --> Internal Service --> mongo-express --> External Service --> Browser

## Topics covered
- minikube
- kubectl
- pods
- nodes
- services - internal and external
- configmaps
- secrets
- k9s

## Installation
- Install Docker from Docker website
- Install minikube ‘brew install minikube’
- Launch Minikube ‘minikube start —driver=Docker —alsologtostderr’
- Check if provisioned correctly with ‘kubectl get nodes’
- Minikube command is only for starting up and deleting the cluster
- For managing the cluster, kubectl is used

## Deployment
- kubectl get pods for all available pods
- kubectl get nodes for all available nodes
- kubectl get services for all available services
- You do not create pods directly, you need to create deployments (an abstraction over pods)
- kubectl create deployment nginx-depl --image=nginx // create sample deployment for nginx
- kubectl logs <pod-name> // to view logs of the pod
- kubectl describe pod <pod-name> // to get a description of the pod status
- kubectl exec -it <pod-name> -- /bin/bash // exec inside container to run commands

### Deployment with yaml file
- kubectl apply -f <deployment.yaml>

### Deployment yaml example
See 'mongo-express.yaml' or 'mongo.yaml' 

### Deployment secret
See 'mongo-secret.yaml'
- Username 'admin'  and password 'password' are base64 encoded strings
- Apply above file using “kubectl apply -f mongo-secret.yaml”
- You can now reference this secret in your deployment.yaml as shown below -
env:
 - name: MONGO_INITDB_ROOT_USERNAME
     valueFrom:
       secretKeyRef:
         name: mongodb-secret
         key: mongo-root-username

## Internal Service 
See 'mongo.yaml' service section for details

## Configmap
See 'mongo-configmap.yaml'

## External Service
See 'mongo-express' service section for details

### Run external service
- Run external service using command ‘minikube service <service-name>
- If you are unable to access the service via the URL, see below ‘Notes’ explanation
- Alternate solution is to port forward from k9s. See below ‘Port forwarding via k9s’ section

## Port Forwarding via k9s - external service
If you are unable to access your your service via the external URL, port forward by -
- Select pod / service
- Shift + f to bring up the port forward option
- Forward needed port and retry accessing the service from outside the cluster

## Notes
If you are running minikube with Docker driver, you will need to do some port-forwarding. Open a separate command line terminal and run the following command (leaving that window open):
`kubectl port-forward service/hello-minikube 54080:8080 `
Now in your original command line window run your service:
`minikube service hello-minikube`

Now you can access http://localhost:54080 and everything should be working correctly.

