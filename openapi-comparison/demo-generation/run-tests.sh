#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Run OpenAPI contract test with Schemathesis"
schemathesis run --url=http://localhost:8000 "$ROOT_DIR/openapi/openapi.yaml"

echo "Run API Blueprint contract test with Dredd"
dredd "$ROOT_DIR/api-blueprint/api.apib" http://localhost:3000

echo "Done"
