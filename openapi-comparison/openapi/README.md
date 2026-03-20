# OpenAPI demo (Library API)

## File chính

- `openapi.yaml`

## Cài đặt tool

```bash
npm i -g @redocly/cli @openapitools/openapi-generator-cli
```

## Validate tài liệu

```bash
redocly lint openapi.yaml
```

## Xem tài liệu dạng HTML tạm thời

```bash
npx @redocly/cli preview-docs openapi.yaml
```

## Sinh code từ OpenAPI

### Sinh FastAPI server stub

```bash
openapi-generator-cli generate \
  -i openapi.yaml \
  -g python-fastapi \
  -o generated-server-fastapi
```

### Sinh TypeScript Axios client

```bash
openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-axios \
  -o generated-client-ts
```

## Sinh/runs test từ spec

Ví dụ contract/fuzz test bằng Schemathesis:

```bash
pip install schemathesis
schemathesis run --url=http://localhost:8000 openapi.yaml
```
