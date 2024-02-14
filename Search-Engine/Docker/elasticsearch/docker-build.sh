#!/bin/bash

set -eu

#docker build --no-cache \


# docker build \
#   -f "$(dirname "$0")/Dockerfile" \
#   -t fn-cicd-basic-api:es \
#   --target runtime \
#   "$(dirname "$0")/."


# docker build \
#   -f "$(dirname "$0")/Dockerfile" \
#   -t fn-cicd-basic-api:test \
#   --target test \
#   "$(dirname "$0")/."


docker build \
  -f "$(dirname "$0")/Dockerfile" \
  -t fn-platform-basic-api:omni_es \
  --target omni_es \
  "$(dirname "$0")/."