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

HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8

HTTP/1.1 409 Conflict
Content-Type: text/plain; charset=utf-8

HTTP/1.1 401 Unauthorized
Content-Type: text/plain; charset=utf-8
```
어드민 계정 정보를 생성할 때 사용합니다