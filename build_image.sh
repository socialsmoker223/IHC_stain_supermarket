#!/bin/sh

image_name=asia.gcr.io/scancer/ihc_supermarket/app
image_tag=latest

full_image_name=${image_name}:${image_tag}
base_image_tag=alpine

docker build  --build-arg BASE_IMAGE_TAG=${base_image_tag} -t "${full_image_name}" .
docker push "$full_image_name"