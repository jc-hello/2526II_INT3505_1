# OpenAPI Comparison - Demo quản lý thư viện

## 1) So sánh OpenAPI, API Blueprint, RAML, TypeSec (TypeSpec)

| Tiêu chí | OpenAPI | API Blueprint | RAML | TypeSec (TypeSpec) |
|---|---|---|---|---|
| Mục tiêu chính | Chuẩn mô tả REST API phổ biến nhất | Viết tài liệu API theo phong cách Markdown dễ đọc | Thiết kế API theo hướng reusable fragments | API-first bằng DSL mạnh kiểu ngôn ngữ lập trình |
| Định dạng | YAML/JSON | Markdown (`.apib`) | YAML (`.raml`) | DSL riêng (`.tsp`) |
| Hệ sinh thái tool | Rất lớn: Swagger UI, OpenAPI Generator, Postman, Schemathesis... | Dredd, Aglio, Apiary, Parser | Anypoint, raml2html, parser RAML | TypeSpec compiler + emitter (OpenAPI, JSON Schema...) |
| Sinh code client/server | Rất mạnh, nhiều ngôn ngữ | Hạn chế hơn OpenAPI | Có, nhưng hệ sinh thái nhỏ hơn | Không trực tiếp nhiều như OpenAPI; thường compile sang OpenAPI rồi generate |
| Test từ spec | Dễ (Dredd, Schemathesis, contract test) | Dredd rất phù hợp | Có thể qua parser/tool chain | Thường test sau khi emit OpenAPI |
| Độ dễ học | Trung bình | Dễ cho người quen Markdown | Trung bình | Trung bình-khó (vì DSL) |
| Khi nên dùng | Cần chuẩn công nghiệp + tự động hóa mạnh | Team muốn docs dễ viết, dễ review | Team đang dùng hệ sinh thái RAML/MuleSoft | Team ưu tiên API modeling nâng cao và tái sử dụng kiểu dữ liệu |

## 2) Cấu trúc bài làm

```text
openapi-comparison/
  openapi/
  api-blueprint/
  raml/
  typesec/
  demo-generation/
```

Mỗi thư mục con có:
- 1 file tài liệu API cho ứng dụng quản lý thư viện
- 1 file `README.md` hướng dẫn cài đặt/chạy

## 3) Demo sinh code/test

Xem tại thư mục `demo-generation/`.

- `generate.sh`: ví dụ lệnh sinh code (client/server) từ các format
- `run-tests.sh`: ví dụ lệnh chạy contract test từ spec
- `README.md`: giải thích chi tiết từng bước

## 4) Gợi ý nộp bài

Khi nộp, gửi link thư mục:

`openapi-comparison`
