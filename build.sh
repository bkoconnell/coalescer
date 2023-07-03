#!/bin/bash
set -euo pipefail

# build test image and run unit tests
docker image build -t coalesce_unittests:v1.0 --target test .
docker container run coalesce_unittests:v1.0

# build image for Coalescer app and run container with mounted volume
docker image build -t coalesce:v1.0 --target app .
docker container run -v "$(pwd)"/output:/app/data coalesce:v1.0