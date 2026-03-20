# API Blueprint demo (Library API)

## File chính

- `api.apib`

## Cài đặt tool

```bash
npm i -g aglio dredd
```

## Render tài liệu HTML

```bash
aglio -i api.apib -o api.html
open api.html
```

## Mock API từ Blueprint

```bash
npx drakov -f api.apib --public
```

Mock server mặc định chạy tại `http://localhost:3000`.

## Chạy test từ Blueprint bằng Dredd

```bash
dredd api.apib http://localhost:3000
```
