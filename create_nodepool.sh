# https://cloud.google.com/composer/docs/how-to/using/using-kubernetes-pod-operator#gcloud
# add the node pool in the k8s cluster which run Cloud Composer
gcloud container node-pools create POOL_NAME \
    --cluster CLUSTER_NAME \
    --project PROJECT_ID \
    --zone ZONE \
    ADDITIONAL_FLAGS 