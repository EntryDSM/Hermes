import os
import hvac


client = hvac.Client(url=f'http://{os.environ["VAULT_ADDR"]}:8200')

if os.environ.get('VAULT_TOKEN'):
    client.token = os.environ['VAULT_TOKEN']
elif os.environ.get('GITHUB_TOKEN'):
    client.auth.github.login(token=os.environ['GITHUB_TOKEN'])

service: str = os.environ["service_name"]
environ: str = os.environ["service_environment"]


class Settings:
    def __init__(self, vault_client: hvac.Client, service_name, environ_name):
        self.client = vault_client
        self.service = service_name
        self.environ = environ_name
        self.database_cred = None

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
            if not self.database_cred:
                self.database_cred = self.client.read(f"database/creds/{self.service}-{self.environ}")["data"].values()
            password, username = self.database_cred
        except Exception as e:
            raise e

        return password, username


settings = Settings(client, service, environ)
