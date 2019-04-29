from typing import Dict

import hvac

from hermes.misc.constants import (GITHUB_TOKEN, RUN_ENV, SERVICE_NAME,
                                   VAULT_ADDRESS, VAULT_TOKEN)


class VaultClient:
    _database_credential = None

    @classmethod
    def initialize(cls):
        cls.client = hvac.Client(url=VAULT_ADDRESS)

        if VAULT_TOKEN:
            cls.client.token = VAULT_TOKEN
        elif GITHUB_TOKEN:
            cls.client.auth.github.login(token=GITHUB_TOKEN)

    def __getattr__(self, item):
        try:
            data = self.client.read(f"service-secret/{RUN_ENV}/{SERVICE_NAME}")["data"]
            return data[item]
        except KeyError as e:
            raise Exception(f"requested key {item} is can't be fetched")
        except Exception as e:
            raise e

    @property
    def database_credential(self) -> Dict[str, str]:
        try:
            if not self._database_credential:
                data = self.client.read(f"database/creds/{SERVICE_NAME}-{RUN_ENV}")[
                    "data"
                ]
                self._database_credential = {
                    "username": data["username"],
                    "password": data["password"],
                }
        except Exception as e:
            raise e

        return self._database_credential


class Setting:
    def __init__(self, vault_client: VaultClient):
        self.vault_client = vault_client

    def __getattr__(self, item):
        return self.vault_client.__getattr__(item)

    @property
    def database_connection_info(self):
        return {
            "use_unicode": True,
            "charset": "utf8mb4",
            "user": self.vault_client.database_credential["username"],
            "password": self.vault_client.database_credential["password"],
            "db": self.vault_client.MYSQL_DATABASE,
            "host": self.vault_client.MYSQL_HOST,
            "port": self.vault_client.MYSQL_PORT,
            "loop": None,
            "autocommit": True,
        }

    @property
    def cache_connection_info(self):
        return {
            "address": f"redis://:{self.vault_client.REDIS_PASSWORD}@{self.vault_client.REDIS_HOST}:{self.vault_client.REDIS_PORT}",  # pylint: disable=line-too-long
            "minsize": 5,
            "maxsize": 10,
        }

    DEBUG = False if RUN_ENV == "prod" else True
    RUN_PORT = 8888
    RUN_HOST = "0.0.0.0"


settings = Setting(VaultClient())  # pylint: disable=invalid-name
