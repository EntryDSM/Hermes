import os

VAULT_ADDRESS = "https://vault.entrydsm.hs.kr"
SERVICE_NAME = os.environ.get("SERVICE_NAME")

VAULT_TOKEN = os.environ.get("VAULT_TOKEN")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

RUN_ENV = os.environ.get("RUN_ENV")

LISTENER_OPTION = [
    "before_server_start",
    "after_server_start",
    "before_server_stop",
    "after_server_stop",
]

LOGO = """
██╗  ██╗███████╗██████╗ ███╗   ███╗███████╗███████╗
██║  ██║██╔════╝██╔══██╗████╗ ████║██╔════╝██╔════╝
███████║█████╗  ██████╔╝██╔████╔██║█████╗  ███████╗
██╔══██║██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ╚════██║
██║  ██║███████╗██║  ██║██║ ╚═╝ ██║███████╗███████║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝                                                        
"""
