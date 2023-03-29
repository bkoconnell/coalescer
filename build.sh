#!/bin/bash
set -euo pipefail

# install requirements.txt (for pytest)
#pip3 install -r requirements.txt

# run unit tests
./unit_test.py

# build image and run container with mounted volume
docker image build -t coalesce:v1.0 .
docker container run -v "$(pwd)"/data:/app/data coalesce:v1.0