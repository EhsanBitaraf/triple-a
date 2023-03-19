#!/bin/sh

set -e

if [ "${1#-}" != "${1}" ] || [ -z "$(command -v "${1}")" ]; then
  set -- cli "$@"
fi

exec "$@"

# https://github.com/dteslya/blog-dockerize-python-cli-tool/blob/main/docker/docker-entrypoint.sh