# RAML demo (Library API)

## File chính

- `api.raml`

## Cài đặt tool

```bash
npm i -g raml2html webapi-parser-cli
```

## Validate/parse RAML

```bash
webapi-parser validate api.raml
```

## Render tài liệu HTML

```bash
raml2html api.raml > api.html
open api.html
```

## Demo test theo hướng contract

Thực tế thường convert RAML sang OpenAPI để tận dụng hệ sinh thái test mạnh hơn:

1. Convert RAML -> OpenAPI bằng tool phù hợp trong team.
2. Chạy test bằng `dredd` hoặc `schemathesis` trên file OpenAPI đã convert.

Ví dụ (sau khi đã có `converted-openapi.yaml`):

```bash
pip install schemathesis
schemathesis run --url=http://localhost:8000 converted-openapi.yaml
```
