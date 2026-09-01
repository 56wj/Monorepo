#!/bin/bash
set -e

REGISTRY="${REGISTRY:-localhost:5000}"
IMAGE="packing-service"
TAG="${1:-latest}"

docker build -t "$REGISTRY/$IMAGE:$TAG" .
docker push "$REGISTRY/$IMAGE:$TAG"

echo "Pushed $REGISTRY/$IMAGE:$TAG"
