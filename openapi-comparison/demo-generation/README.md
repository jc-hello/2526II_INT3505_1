# Demo sinh code/test từ tài liệu API

Thư mục này minh họa cách sinh code và chạy test contract từ các file tài liệu API.

## Yêu cầu cài đặt

```bash
npm i -g @openapitools/openapi-generator-cli @typespec/compiler @typespec/openapi3 dredd
pip install schemathesis
```

## Quy trình demo

### A. Sinh code

```bash
cd demo-generation
bash generate.sh
```

Kết quả sinh code nằm trong `demo-generation/out/`.

### B. Chạy test từ spec

Chuẩn bị mock/implementation chạy trước:

- OpenAPI target: `http://localhost:8000`
- API Blueprint mock (Drakov): `http://localhost:3000`

Sau đó chạy:

```bash
cd demo-generation
bash run-tests.sh
```

## Ghi chú

- OpenAPI: có hệ sinh thái codegen/test mạnh nhất.
- API Blueprint: tài liệu dễ đọc, Dredd test tốt.
- RAML: thường kết hợp tool nội bộ hoặc convert sang OpenAPI để tận dụng toolchain.
- TypeSec/TypeSpec: mạnh ở modeling, thường emit OpenAPI rồi codegen/test.
