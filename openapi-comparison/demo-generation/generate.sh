#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "[1/3] Generate code from OpenAPI"
openapi-generator-cli generate \
  -i "$ROOT_DIR/openapi/openapi.yaml" \
  -g python-fastapi \
  -o "$ROOT_DIR/demo-generation/out/openapi-server"

echo "[2/3] Compile TypeSpec to OpenAPI"
(cd "$ROOT_DIR/typesec" && tsp compile .)

echo "[3/3] Generate client from emitted OpenAPI"
openapi-generator-cli generate \
  -i "$ROOT_DIR/typesec/tsp-output/@typespec/openapi3/openapi.yaml" \
  -g typescript-axios \
  -o "$ROOT_DIR/demo-generation/out/typesec-client"

echo "Done. Generated output in: $ROOT_DIR/demo-generation/out"
