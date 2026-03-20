# TypeSec (TypeSpec) demo - Library API

## File chính

- `main.tsp`
- `tspconfig.yaml`

## Cài đặt tool

```bash
npm i -g @typespec/compiler @typespec/openapi3
```

## Compile TypeSpec -> OpenAPI

```bash
tsp compile .
```

Sau khi compile, file OpenAPI thường nằm trong `tsp-output/`.

## Demo sinh code/test

Vì TypeSpec thường emit sang OpenAPI, quy trình phổ biến là:

1. Compile ra OpenAPI.
2. Dùng OpenAPI Generator để sinh code.
3. Dùng Schemathesis/Dredd để test contract.

Ví dụ:

```bash
npx @openapitools/openapi-generator-cli generate \
  -i tsp-output/@typespec/openapi3/openapi.yaml \
  -g python-fastapi \
  -o generated-server
```
