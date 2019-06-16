# Hermes
![Python: 3.7](https://img.shields.io/badge/python-3.7-blue.svg)
[![Code Style: Black](https://badgen.net/badge/code%20style/black/black)](https://github.com/ambv/black)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/186943feb6d546b18884e4548915f136)](https://app.codacy.com/app/NovemberOscar/Hermes?utm_source=github.com&utm_medium=referral&utm_content=EntryDSM/Hermes&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.org/EntryDSM/Hermes.svg?branch=master)](https://travis-ci.org/EntryDSM/Hermes)
[![codecov](https://codecov.io/gh/EntryDSM/Hermes/branch/master/graph/badge.svg)](https://codecov.io/gh/EntryDSM/Hermes)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=EntryDSM_Hermes&metric=coverage)](https://sonarcloud.io/dashboard?id=EntryDSM_Hermes)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=EntryDSM_Hermes&metric=code_smells)](https://sonarcloud.io/dashboard?id=EntryDSM_Hermes)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=EntryDSM_Hermes&metric=duplicated_lines_density)](https://sonarcloud.io/dashboard?id=EntryDSM_Hermes)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=EntryDSM_Hermes&metric=ncloc)](https://sonarcloud.io/dashboard?id=EntryDSM_Hermes)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=EntryDSM_Hermes&metric=alert_status)](https://sonarcloud.io/dashboard?id=EntryDSM_Hermes)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=EntryDSM_Hermes&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=EntryDSM_Hermes)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=EntryDSM_Hermes&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=EntryDSM_Hermes)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=EntryDSM_Hermes&metric=sqale_index)](https://sonarcloud.io/dashboard?id=EntryDSM_Hermes)

![](https://seeklogo.com/images/H/Hermes-logo-C6741CE724-seeklogo.com.png)

Handles all EntryDSM user(admin, applicant) related functions on the EntryDSM platform

## Getting Started

By follow these instructions, you can run and test hermes on your environment

### configure pyenv

> $ pyenv virtualenv 3.7.2 hermes

> $ pyenv local hermes

> $ pip install -r requirements.txt

> $ pip install -r requirements_dev.txt

### Running

For run this, you must configure some environment variables.

Let's configure. if you want to run in the pycharm, configure below environment variables to pycharm run setting. `Run/Debug Configurations > Environment Variables`

> $ export VAULT_ADDR=vault.entrydsm.hs.kr

> $ export GITHUB_TOKEN={{your read::org permission github token}}

> $ export SERVICE_NAME=hermes

> $ export RUN_ENV={{test or prod}}

### Testing

hermes uses pytest.

> **NOTICE!**
>
>hermes uses `pytest-mysql` and `pytest-redis`. these extensions require executable for test setup(they are demonizing executable while testing).
>
>so, you must install mysql(5.7) and redis executable.
>

For run the tests. you must install everything on `requirements_dev.txt` via pip.

after install every test requirements. just run this command.

> $ pytest --cov=./hermes ./tests

There's probably no problem.
 but if you get trouble, follow the below instructions.

#### Cofigure test arguments

every configurations are in the  `pytest.ini` 

- Known case I: pytest-mysql configuration(MacOS)

    you can see this part on the pytest.ini

    ```
    ;mysql_mysqld = /usr/local/opt/mysql@5.7/bin/mysqld
    ;mysql_mysqld_safe = /usr/local/opt/mysql@5.7/bin/mysqld_safe
    ;mysql_install_db = /usr/local/opt/mysql@5.7/bin/mysql_install_db
    ;mysql_admin = /usr/local/opt/mysql@5.7/bin/mysqladmin
    ```

    un-annotate this. 

## Stack
- Sanic - A async web framework
- marshmallow - A lightweight schema valiator
- MySQL - Most popular RDBMS
- Redis - In-memory DB for caching
- Vault - Super secure secret backend
- Travis CI - Hosted CI/CD pipeline
- Docker - Most popular container platform

## Versioning
```
{Major}.{Minor}.{Patch}
```
ex: 0.2.3

- Major: without subcompatibility
- Minor: with partial subcompatibility
- Patch: with full subcompatibility

## Maintainer

- Seonghyeon Kim - [NovemberOscar](https://github.com/NovemberOscar)
