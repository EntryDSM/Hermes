---
title: API Reference

language_tabs: # must be one of https://git.io/vQNgJ
  - http

toc_footers:
  - <a href='https://github.com/EntryDSM/Hermes'>Go to repository</a>
  - <a href='https://github.com/lord/slate'>Documentation Powered by Slate</a>

includes:
  - errors

search: true
---

# 개요

에르메스는 계정 정보를 관리하는 서비스입니다. 유저와 어드민 정보를 담당하고 있습니다.

# /admin
## POST

```http
POST /api/v1/admin HTTP/1.1
Host: api.entrydsm.hs.kr
User-Agent: your-client/1.0
Content-Type: application/json
Accept: */*
{
	"id": "entry2019root",
	"name": "성현김",
	"password": "asdf",
	"type": 1,
	"email": "asdf@gmail.com"
}
```

> Response will be like this:

```
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8

HTTP/1.1 400 Bad Request
Content-Type: text/plain; charset=utf-8

HTTP/1.1 409 Conflict
Content-Type: text/plain; charset=utf-8

HTTP/1.1 404 Not Found
Content-Type: text/plain; charset=utf-8

HTTP/1.1 401 Unauthorized
Content-Type: text/plain; charset=utf-8
```
어드민 계정 정보를 생성할 때 사용합니다

### Attributes

| name     | type | description                                 | required |
|----------|------|---------------------------------------------|----------|
| id       | str  | admin id                                    |O         |
| name     | str  | admin name                                  |O         |
| password | str  | password                                    |O         |
| type     | int  | admin type  `0: ROOT 1: ADMIN 2: INTERVIEW` |O         |
| email    | str  | admin email                                 |O         |

<aside class="notice">
type에 올바른 정수가 들어가 있는지 확인해 주세요
</aside>

# /admin/batch
## GET

```http
POST /api/v1/admin/batch HTTP/1.1
Host: api.entrydsm.hs.kr
User-Agent: your-client/1.0
```

> Response will be like this:

```
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
[
  {
    "id": "entry2019root",
    "name": "성현김",
    "email": "asdf@gmail.com",
    "type": 1
  },
  {
    "id": "entry2019admin",
    "name": "준모연",
    "email": "qwer@gmail.com",
    "type": 2
  }
]

HTTP/1.1 401 Unauthorized
Content-Type: text/plain; charset=utf-8
```
다량의 어드민 정보를 가져올 때 사용합니다.

### Query Parameters

| name     | type | description                                 | required |
|----------|------|---------------------------------------------|----------|
| id       | str  | admin id                                    |X         |
| name     | str  | admin name                                  |X         |
| type     | int  | admin type  `0: ROOT 1: ADMIN 2: INTERVIEW` |X         |
| email    | str  | admin email                                 |X         |

# /admin/<admin_id>
## GET

```http
GET /api/v1/admin/entry2019admin HTTP/1.1
Host: api.entrydsm.hs.kr
User-Agent: your-client/1.0
```

> Response will be like this:

```
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
{
  "id": "entry2019admin",
  "name": "준모연",
  "email": "qwer@gmail.com",
  "type": 2
}

HTTP/1.1 404 Not Found
Content-Type: text/plain; charset=utf-8

HTTP/1.1 401 Unauthorized
Content-Type: text/plain; charset=utf-8
```
하나의 어드민 정보를 가져옵니다

<aside class="notice">
조회할 수 없다면 404를 반환합니다
</aside>

## PATCH

```http
PATCH /api/v1/admin/entry2019admin HTTP/1.1
Host: api.entrydsm.hs.kr
User-Agent: your-client/1.0
{
	"id": "entry2019root2",
	"name": "태민차",
	"email": "qwer@gmail.com"
}
```

> Response will be like this:

```
HTTP/1.1 204 No Content
Content-Type: text/plain; charset=utf-8

HTTP/1.1 404 Not Found
Content-Type: text/plain; charset=utf-8

HTTP/1.1 401 Unauthorized
Content-Type: text/plain; charset=utf-8
```
하나의 어드민 정보를 패치합니다

### Attributes

| name     | type | description                                 | required |
|----------|------|---------------------------------------------|----------|
| id       | str  | admin id                                    |X         |
| name     | str  | admin name                                  |X         |
| password | str  | password                                    |X         |
| type     | int  | admin type  `0: ROOT 1: ADMIN 2: INTERVIEW` |X         |
| email    | str  | admin email                                 |X         |


<aside class="notice">
조회할 수 없다면 404를 반환합니다
</aside>
