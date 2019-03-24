---
title: API Reference

language_tabs: # must be one of https://git.io/vQNgJ
  - http

toc_footers:
  - <a href='https://github.com/EntryDSM/Hermes'>Go to repository</a>
  - <a href='https://github.com/lord/slate'>Documentation Powered by Slate</a>

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
HTTP/1.1 201 Created
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

### Permisions
|||
|--------------------|-------|
| public             | false |
| inter-service call | true  |

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
Content-Type: application/json; charset=utf-8
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

### Permisions
|||
|--------------------|-------|
| public             | false |
| inter-service call | true  |

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
Content-Type: application/json; charset=utf-8
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

### Permisions
|||
|--------------------|-------|
| public             | false |
| inter-service call | true  |

<aside class="notice">
조회할 수 없다면 404를 반환합니다
</aside>

## PATCH

```http
PATCH /api/v1/admin/entry2019admin HTTP/1.1
Host: api.entrydsm.hs.kr
User-Agent: your-client/1.0
{
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

### Permisions
|||
|--------------------|-------|
| public             | false |
| inter-service call | true  |

### Attributes

| name     | type | description                                 | required |
|----------|------|---------------------------------------------|----------|
| name     | str  | admin name                                  |X         |
| password | str  | password                                    |X         |
| type     | int  | admin type  `0: ROOT 1: ADMIN 2: INTERVIEW` |X         |
| email    | str  | admin email                                 |X         |


<aside class="notice">
조회할 수 없다면 404를 반환합니다
</aside>

## DELETE

```http
DELETE /api/v1/admin/entry2019root HTTP/1.1
Host: api.entrydsm.hs.kr
User-Agent: your-client/1.0
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
하나의 어드민 정보를 삭제합니다.

### Permisions
|||
|--------------------|-------|
| public             | false |
| inter-service call | true  |

<aside class="notice">
조회할 수 없다면 404를 반환합니다
</aside>


# /applicant
## POST

```http
POST /api/v1/applicant HTTP/1.1
Host: api.entrydsm.hs.kr
User-Agent: your-client/1.0
Content-Type: application/json
Accept: */*
{
	"email": "asdf@gmail.com",
	"password": "asdf",
}
```

> Response will be like this:

```
HTTP/1.1 201 Created
Content-Type: text/plain; charset=utf-8

HTTP/1.1 400 Bad Request
Content-Type: text/plain; charset=utf-8

HTTP/1.1 409 Conflict
Content-Type: text/plain; charset=utf-8

HTTP/1.1 401 Unauthorized
Content-Type: text/plain; charset=utf-8
```
어드민 계정 정보를 생성할 때 사용합니다

### Permisions
|||
|--------------------|-------|
| public             | false |
| inter-service call | true  |

### Attributes

| name     | type | description        | required |
|----------|------|--------------------|----------|
| email    | str  | applicant email    |O         |
| password | str  | password           |O         |

<aside class="notice">
pre-user를 verify한 후 applicant로 만들기 위해 사용합니다. 이메일과 비밀번호 이외의 다른 정보는 PATCH /applicant/{{id}} 에서 생성/수정합니다.
</aside>

# /applicant/batch
## GET

```http
POST /api/v1/applicant/batch HTTP/1.1
Host: api.entrydsm.hs.kr
User-Agent: your-client/1.0
```

> Response will be like this:

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
[
  {
    "email": "asdf@gmail.com",
    "name": "성현김",
    "sex": 0,
    "birth_date": "2001-12-17",
    "tel": "01023456789", 
    "parent_name": "김보호",
    "parent_tel": "01012345678",
    "address": "서울시 서대문구 xx로 xx",
    "post_code": 11111,
    "image_path": {{uuid here}}
  },
  {
    "email": "qwer@gmail.com",
    "name": "준모연",
    "address": "서울시 서대문구 xx로 xx",
    "post_code": 11111
  }
]

HTTP/1.1 401 Unauthorized
Content-Type: text/plain; charset=utf-8
```
다량의 유저 정보를 가져올 때 사용합니다. 정보가 존재하지 않는 필드들은 포함되지 않습니다.

image path는 `cdn.entrydsm.hs.kr/{{image path}}` 형식으로 사용하시면 됩니다.

### Permisions
|||
|--------------------|-------|
| public             | false |
| inter-service call | true  |

### Query Parameters

| name          | type      | description                                 | required |
|---------------|-----------|---------------------------------------------|----------|
| email         | str       | admin email                                 |X         |
| name          | str       | admin name                                  |X         |
| sex           | int       | sex                                         |X         |
| birth_date    | datetime  | birth date                                  |X         |
| tel           | str       | phone number                                |X         |
| parent_name   | str       | parent_name                                 |X         |
| address       | str       | address                                     |X         |
| post_code     | str       | post code (length 5)                        |X         |

# /applicant/<user_id>
## GET
```http
GET /api/v1/applicant/asdf@gmail.com HTTP/1.1
Host: api.entrydsm.hs.kr
User-Agent: your-client/1.0
```

> Response will be like this:

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
  "email": "asdf@gmail.com",
  "name": "성현김",
  "sex": 0,
  "birth_date": "2001-12-17",
  "tel": "01023456789", 
  "parent_name": "김보호",
  "parent_tel": "01012345678",
  "address": "서울시 서대문구 xx로 xx",
  "post_code": 11111,
  "image_path": {{uuid here}}
}

HTTP/1.1 404 Not Found
Content-Type: text/plain; charset=utf-8

HTTP/1.1 401 Unauthorized
Content-Type: text/plain; charset=utf-8
```
하나의 지원자 정보를 가져옵니다. 정보가 존재하지 않는 필드들은 포함되지 않습니다.

image path는 `cdn.entrydsm.hs.kr/{{image path}}` 형식으로 사용하시면 됩니다.

### Permisions
|||
|--------------------|-------|
| public             | true  |
| inter-service call | true  |

<aside class="notice">
조회할 수 없다면 404를 반환합니다
</aside>

## PATCH

```http
PATCH /api/v1/applicant/asdf@gmail.com HTTP/1.1
Host: api.entrydsm.hs.kr
User-Agent: your-client/1.0
{
	"parent_name": "김부모",
  "tel": "01011223344"
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
하나의 지원자 정보를 패치합니다

### Permisions
|||
|--------------------|-------|
| public             | true  |
| inter-service call | true  |

### Attributes

| name          | type      | description                                 | required |
|---------------|-----------|---------------------------------------------|----------|
| name          | str       | admin name                                  |X         |
| sex           | int       | sex                                         |X         |
| birth_date    | datetime  | birth date                                  |X         |
| tel           | str       | phone number                                |X         |
| parent_name   | str       | parent_name                                 |X         |
| address       | str       | address                                     |X         |
| post_code     | str       | post code (length 5)                        |X         |


<aside class="notice">
조회할 수 없다면 404를 반환합니다
</aside>

## DELETE
```http
DELETE /api/v1/applicant/asdf@gmail.com HTTP/1.1
Host: api.entrydsm.hs.kr
User-Agent: your-client/1.0
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
하나의 지원자 정보를 삭제합니다.

### Permisions
|||
|--------------------|-------|
| public             | false |
| inter-service call | true  |

<aside class="notice">
조회할 수 없다면 404를 반환합니다
</aside>

# /authentication
## POST

```http
POST /api/v1/authentication HTTP/1.1
Host: api.entrydsm.hs.kr
User-Agent: your-client/1.0
Content-Type: application/json
Accept: */*
{
  "email": "asdf@gmail.com",
  "password": "asdf",
  "level": "user"
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

HTTP/1.1 401 Unauthorized
Content-Type: text/plain; charset=utf-8
```
인증을 수행합니다.
### Permisions
|||
|--------------------|-------|
| public             | false |
| inter-service call | true  |

### Attributes

| name     | type | description            | required |
|----------|------|------------------------|----------|
| email    | str  | applicant email        |O         |
| password | str  | password               |O         |
| level    | str  | `admin` or `applicant` |O         |


<aside class="notice">
Chanel을 위한 API 입니다. 200 OK가 들어온다면 보낸 정보를 토대로 토큰을 생성하면 됩니다.
</aside>