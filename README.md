# Hermes
![Python: 3.7](https://img.shields.io/badge/python-3.7-blue.svg)
[![Code Style: Black](https://badgen.net/badge/code%20style/black/black)](https://github.com/ambv/black)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/186943feb6d546b18884e4548915f136)](https://app.codacy.com/app/NovemberOscar/Hermes?utm_source=github.com&utm_medium=referral&utm_content=EntryDSM/Hermes&utm_campaign=Badge_Grade_Dashboard)

![](https://seeklogo.com/images/H/Hermes-logo-C6741CE724-seeklogo.com.png)

Handles all EntryDSM user(admin, applicant) related functions on the EntryDSM platform

## Getting Started

By follow these instrucction, you can run hermes on the local for dev&test purpose.

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

hermes is using pytest.

For run the tests. you must install everything on `requirements_dev.txt` via pip.

after install every test requirements. just run this command.

> $ pytest --cov=hermes

There's probably no problem.
 but if you get trouble, follow the below instructuons.

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

## Versioning
```
{Major}.{Minor}.{Patch}
```
ex: 0.2.3

- Major: without subcompatibility
- Minor: with partial subcompatibility
- Patch: with full subcompatibility

## Authors

- Seonghyeon Kim - [NovemberOscar](https://github.com/NovemberOscar)
