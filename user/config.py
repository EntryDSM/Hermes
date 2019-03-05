import os
import hvac

client = hvac.Client(url=f'http://{os.environ["VAULT_ADDR"]}:8200', token=os.environ['VAULT_TOKEN'])
service: str = os.environ["service_name"]
environ: str = os.environ["service_environment"]


class Settings:
    def __init__(self, vault_client: hvac.Client, service_name, environ_name):
        self.client = vault_client
        self.service = service_name
        self.environ = environ_name

    def __getattr__(self, item):
        try:
            data = self.client.read(f'service-secret/{self.environ}/{service}')["data"]
            data = data[item]
        except KeyError as e:
            raise Exception(f"requested key {item} is can't be fetched")
        except Exception as e:
            raise e

        return data

    def get_database_cred(self):
        try:
            database_cred = self.client.read(f"database/creds/entry-{self.environ}")
            password, username = database_cred
        except Exception as e:
            raise e

        return database_cred


settings = Settings(client, service, environ)
